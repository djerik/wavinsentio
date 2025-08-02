# Wavin Sentio
> API Wrapper for Wavin Sentio underfloor heating system.

Enables you to query status of thermostats and change target temperature

## Usage example

ws = wavinsentio.WavinSentio("username","password")

## Release History

* 0.1.0
    * The first proper release
* 0.2.0
    * Added setTemperature, setProfile and refresh token logic
* 0.2.1
    * PyPi push
* 0.2.2
    * Cleaned folder structure
* 0.2.3
    * Fixed error handling
* 0.3.0
    * Added get_location including outdoor temperature
* 0.4.1
    * Changed base URL for Wavin Sentio service
* 0.5.0
    * Àdded support for new Sentio v18 firmware
* 0.5.1
    * Fix StandbyMode and other small fixes
* 0.5.2
    * Added outdoor temperature and other small fixes
* 0.5.3
    * Fix for empty vacationModeUntili