# Alpha Vantage Integration for Home Assistant

<p align="center">
  <img src="https://raw.githubusercontent.com/alaschgari/hacs-alpha-vantage/main/logo.png" alt="Alpha Vantage Logo" width="200" height="200">
</p>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-orange.svg)](https://www.buymeacoffee.com/alaschgari)

This custom integration for Home Assistant allows you to track stock and financial market data using the Alpha Vantage API.

> [!NOTE]
> Home Assistant already has a native Alpha Vantage integration. This project is a **custom integration** that provides an alternative way to track stock data with a focus on ease of use via the UI and specific sensor configurations.

## Prerequisites
To use this integration, you need an **Alpha Vantage API Key**.
- You can get a free API key by signing up at [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key).
- Once registered, you will receive your API key via email.

## Features
- Real-time price tracking for global stocks, ETFs, and mutual funds.
- Day High, Day Low, and Previous Close sensors.
- Volume and Change Percent tracking.
- Easy configuration via Home Assistant UI.
- Support for multiple symbols (comma-separated).

## Supported API Endpoints
This integration utilizes the following Alpha Vantage API function:
- **Global Quote**: `GLOBAL_QUOTE` (Price, Volume, High, Low, Change)

## Installation via HACS
1. Open HACS in your Home Assistant instance.
2. Click on "Integrations".
3. Click the three dots in the upper right corner and select "Custom repositories".
4. Add the URL of this repository (`https://github.com/alaschgari/hacs-alpha-vantage`) and select "Integration" as the category.
5. Click "Add" and then install the "Alpha Vantage" integration.
6. Restart Home Assistant.

## Configuration
1. Go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Alpha Vantage**.
4. Enter your **API Key** (from [alphavantage.co](https://www.alphavantage.co/)) and the **Symbols** (comma-separated, e.g., `AAPL,TSLA,MSFT`) you want to track.

## Support

If you find this integration useful and want to support its development, you can buy me a coffee! Your support is greatly appreciated and helps keep this project alive and updated.

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-orange.svg?style=for-the-badge&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/alaschgari)

## Disclaimer

This integration is an **unofficial** project and is **not** affiliated, associated, authorized, endorsed by, or in any way officially connected with Alpha Vantage, or any of its subsidiaries or its affiliates. The official Alpha Vantage website can be found at [https://www.alphavantage.co](https://www.alphavantage.co).

This project is provided "as is" by a private individual for educational and personal use only. **No warranty** of any kind, express or implied, is made regarding the accuracy, reliability, or availability of this integration. Use it at your own risk. The author assumes no responsibility or liability for any errors or omissions in the content of this project or for any damages arising from its use.
