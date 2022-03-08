# Pi-Door
## STEM Door Security Project

![STEM Project Stamp](cloud.png)

--- 

The Pi-Door project controls the door security system in the Ashland High School STEM room. It includes a web service that serves both an admin control page and a web display for the screen on the window. The code for this project is highly specialized and requires the exact hardware to work. Several pins on the Raspberry Pi device are required for use with peripherals, but the pin numbers can be assigned in the configuration file. All files are loaded and created dynamically by the software, but the repository contains the settings we use by default. Deploying a similar system with this code may require changes to the peripheral code, but everything else should work well.

---

## TO-DO List

- Implement temperature and humidity readings via Arduino sensors through serial connection
- Implement serial connection auto-detection features
- Implement HTTPS security and password authentication for management page
- Implement user friendly control schemes
- Implement better graphics and animations on kiosk page
- Implement more hardened networking implementation
- Convert development server to production implementation
- Implement flexible API for remote control
- Implement dynamic network discovery protocol through Avahi, etc.
- Implement better software version control
