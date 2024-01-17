# Trading Platform APIs
An advanced trading platform designed for both administrators and users, offering a wide array of features for seamless and efficient trading experiences.

## Table of Contents
- [Features](#features)
  - [Admin Portal](#admin-portal)
  - [User Portal](#user-portal)
  - [Trading Portals](#trading-portals)
    - [Live Trading](#live-trading)
    - [Paper Trading](#paper-trading)
  - [Exchange Functionalities](#exchange-functionalities)
    - [Binance Spot](#binance-spot)
    - [Binance Future](#binance-future)
  - [Data Streams](#data-streams)
- [Installation](#installation)
- [Configuration](#configuration)
- [Run the Application](#run-the-application)
- [Contributions](#contributions)
- [License](#license)


## Features

### Admin Portal
- Full website access
- User management
- Control over APIs, Exchanges, and Platforms

### User Portal
- Limited website access
- Specific trading capabilities



### Trading Portals

#### Live Trading
- Direct trading on exchanges with real money
- Integration with Binance Spot and Binance Future

#### Paper Trading
- Simulated trading on exchanges using dummy money
- Facilitates learning risk and money management



### Exchange Functionalities

#### Binance Spot
- Live and Paper Trading APIs
- Adheres to Binance Exchange Portal limitations
- User validation via API and Secret Key

#### Binance Future
- Live and Paper Trading APIs
- Compliance with Binance Exchange Portal requirements
- User validation through API and Secret Key

### Data Streams
- MongoDB Change Streams
- Real-time price tracking
- Continuous database updates for effective trade monitoring



## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ShhRey/TradingPlatform.git
   
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configuration:
Obtain API and Secret Keys from Binance for both Spot and Future.
Update configuration files with the obtained keys.
Run the Application
```bash
python main.py
```
