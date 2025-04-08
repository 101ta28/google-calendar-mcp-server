#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# APIに要求する権限を指定
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# === 設定ファイル ===

# プロジェクトディレクトリ内のパスを設定
BASE_DIR = Path(__file__).resolve().parent

# 認証情報ファイルとトークンファイルのパスを設定
CREDENTIALS_PATH = BASE_DIR / "credentials.json"
TOKEN_PATH = BASE_DIR / "token.json"


def authenticate_google_calendar():
    """Google Calendar APIに認証し、token.jsonを生成する"""
    creds = None

    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with TOKEN_PATH.open("w") as token:
            token.write(creds.to_json())
    return creds


if __name__ == "__main__":
    print("[INFO] Generating token.json...")
    authenticate_google_calendar()
    print("[INFO] token.json generated successfully.")
