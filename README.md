# About
A simple python script to manage the Parental Control system of a PLDT Home DSL router.

I use the Parental Controls feature of my PLDT Home DSL router to control the times that devices are allowed to connect to the internet. It's mostly used for making sure that kids do not go past their bedtime surfing the net. Accessing and using the router's dashboard is slow and inneficient so I decided to make a script to do it automatically.

### A technical note:
This script sends an http request to 192.168.1.1 containing the commands as parameters. I got these commands by observing the POST requests when a command is excuted from the router's dashboard. It's very inelegant but it works.

## Arguments
First argument: The command to invoke
Check out ACCEPTED_COMMANDS constant variable for full list of commands

Second argument: Device name/s to exclude. 
Separated by a comma. For example, "device1,device2".

## Sample usages
```./net-parental-control.py enable```

```./net-parental-control.py lockdown device3,device4```

## Devices File
The devices.json file should look like the one below:
```
{
    "device1" : {
	"mac" : "00:01:02:03:04:05",  # The mac address of the device
	"enableTimeFrom" : "09:30",   # The starting time to enable this device
	"enableTimeTo" : "23:00"      # The time to disable this device
    },
    "device2" : {
	"mac" : "00:01:02:03:04:05",
	"enableTimeFrom" : "14:00",
	"enableTimeTo" : "20:00"
    }
}
```
