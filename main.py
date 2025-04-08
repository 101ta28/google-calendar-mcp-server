#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import datetime
import zoneinfo
from pathlib import Path
from mcp.server.fastmcp import FastMCP, Context
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

mcp = FastMCP("google-calendar-mcp-server")

# APIに要求する権限を指定
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# === 設定ファイル ===

SETTINGS_FILE = "calendar_settings.json"


def load_calendar_ids(settings_file):
    """設定ファイルからカレンダーIDを読み込む"""
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)
    return settings.get("calendar_ids", {})


# カレンダータイプとIDのマッピング
CALENDAR_IDS = load_calendar_ids(SETTINGS_FILE)

# === Google Calendar API ===


def authenticate_google_calendar():
    """Google Calendar APIに認証する"""
    creds = None

    base_dir = Path(__file__).resolve().parent

    token_path = base_dir / "token.json"
    credentials_path = base_dir / "credentials.json"

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with token_path.open("w") as token:
            token.write(creds.to_json())
    return creds


def search_events(
    service,
    start_date=None,
    end_date=None,
    location=None,
    summary=None,
    calendar_type=None,
    description=None,
):
    """
    指定された検索条件に基づいてイベントを検索し、詳細を返す。
    """
    print("イベントを検索中")

    def to_rfc3339(date_str):
        dt = datetime.datetime.fromisoformat(date_str)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=zoneinfo.ZoneInfo("Asia/Tokyo"))
        return dt.isoformat()

    if start_date:
        # start_dateの時間部分が欠けている場合、00:00:00を追加
        if len(start_date) == 10:
            start_date += "T00:00:00"
        time_min = to_rfc3339(start_date)
    else:
        time_min = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()

    if end_date:
        # end_dateの時間部分が欠けている場合、23:59:59を追加
        if len(end_date) == 10:
            end_date += "T23:59:59"
        time_max = to_rfc3339(end_date)
    else:
        time_max = None  # 終了日時が指定されていない場合はNone

    # カレンダータイプの処理
    if calendar_type and calendar_type.lower() in CALENDAR_IDS:
        # 特定のカレンダーが指定された場合、そのカレンダーのみ検索
        calendar_id = CALENDAR_IDS[calendar_type.lower()]
        return search_calendar_events(
            service, calendar_id, time_min, time_max, location, summary, description
        )
    else:
        # カレンダータイプの指定がない、または "all" の場合、すべてのカレンダーを検索
        all_events = []
        for cal_type, cal_id in CALENDAR_IDS.items():
            if cal_id:  # 設定ファイルに設定されている場合のみ
                print(f"カレンダー {cal_type} を検索中...")
                cal_events = search_calendar_events(
                    service, cal_id, time_min, time_max, location, summary, description
                )
                all_events.extend(cal_events)
        return all_events


def search_calendar_events(
    service, calendar_id, time_min, time_max, location, summary, description
):
    """特定のカレンダーからイベントを検索"""
    try:
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                **({"timeMax": time_max} if time_max else {}),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print(f"カレンダー {calendar_id} に条件に一致するイベントはありません。")
            return []

        # 条件に一致するイベントの詳細をリストに格納
        filtered_events = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            event_summary = event.get("summary", "タイトルなし")
            event_location = event.get("location", "場所なし")
            event_calendar_type = event.get("organizer", {}).get(
                "displayName", "カレンダーの種類なし"
            )
            event_description = event.get("description", "説明なし")

            # 検索条件に一致するか確認
            if (
                (location and location not in event_location)
                or (summary and summary not in event_summary)
                or (description and description not in event_description)
            ):
                continue

            filtered_events.append(
                {
                    "start": start,
                    "end": end,
                    "summary": event_summary,
                    "location": event_location,
                    "calendar_type": event_calendar_type,
                    "description": event_description,
                    "calendar_id": calendar_id,
                }
            )

        return filtered_events
    except HttpError as error:
        print(f"カレンダー {calendar_id} の検索中にエラーが発生しました: {error}")
        return []


# === MCPツール ===


@mcp.tool()
def search_all_calendars(
    ctx: Context,
    start_date: str = None,
    end_date: str = None,
    location: str = None,
    summary: str = None,
    description: str = None,
) -> str:
    """すべてのカレンダーからイベントを検索するツール"""
    creds = authenticate_google_calendar()
    try:
        service = build("calendar", "v3", credentials=creds)
        events = search_events(
            service, start_date, end_date, location, summary, "all", description
        )
        return json.dumps(events, ensure_ascii=False)
    except HttpError as error:
        return json.dumps(
            {"error": f"エラーが発生しました: {error}"}, ensure_ascii=False
        )


@mcp.tool()
def search_calendar_events_by_type(
    ctx: Context,
    calendar_type: str,
    start_date: str = None,
    end_date: str = None,
    location: str = None,
    summary: str = None,
    description: str = None,
) -> str:
    """特定のカレンダータイプからイベントを検索するツール"""
    if (
        calendar_type.lower() not in CALENDAR_IDS
        or not CALENDAR_IDS[calendar_type.lower()]
    ):
        return json.dumps(
            {"error": f"カレンダーIDが設定されていません: {calendar_type}"},
            ensure_ascii=False,
        )

    creds = authenticate_google_calendar()
    try:
        service = build("calendar", "v3", credentials=creds)
        events = search_events(
            service, start_date, end_date, location, summary, calendar_type, description
        )
        return json.dumps(events, ensure_ascii=False)
    except HttpError as error:
        return json.dumps(
            {"error": f"エラーが発生しました: {error}"}, ensure_ascii=False
        )


if __name__ == "__main__":
    print("[INFO] MCPサーバー起動中...")
    mcp.run()
