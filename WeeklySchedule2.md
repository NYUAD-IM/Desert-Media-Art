# Weekly Schedule - Weeks 8-14

[Weekly Schedule Spreadsheet](https://docs.google.com/spreadsheets/d/1UHKrTE_1LE3XZrwBPc6z2o0C35TFm3rHhnjkTC5FYvE/edit?usp=sharing)

- [Week 1](WeeklySchedule.md#week-11) – Introduction / Media art outside
- [Week 2](WeeklySchedule.md#week-21) – CircuitPython / Workshop: CircuitPython
- [Week 3](WeeklySchedule.md#week-31) – Desert Ecology and Culture / Workshop: Motors, Sound, Light
- [Week 4](WeeklySchedule.md#week-41) – 2D Design for Laser Cutting / Workshop: 3D Printing
- [Week 5](WeeklySchedule.md#week-51) – Workshop: Laser Cutting / Workshop: Sensors
- [Week 6](WeeklySchedule.md#week-61) – Outdoor Interaction Design / Idea Lab
- [Week 7](WeeklySchedule.md#week-71) – Idea Lab Presentations / Workshop: Idea Development
- FALL BREAK
- [Week 8](#week-81) – Class visit / Electronics in the Desert / Workshop: LEDs and Servos
- [DESERT SITE VISIT](#desert-site-visit) – Sunday November 5
- [Week 9](#week-91) – 3D Design with Tinkercad / Project Final Proposal Presentations
- [Week 10](#week-101) – Requested topics / Work session
- [Week 11](#week-111) – Telling your story – Exhibition Installations / Rapid Prototyping project review – Work session
- [Week 12](#week-121) – Storyboard Presentations / Prototype Presentations – Work Session
- [FIELD INSTALLATION](#field-installation) – Sunday November 26
- [Week 13](#week-131) – Field work debrief
- [Week 14](#week-141) – Work session: Installation and video production / Present Final Project, Course Review
- [IM SHOW](#im-show) – Show Final Installation / Update installation documentation

Note: Exact due dates for assignments and readings are indicated in Brightspace

---

[Desert Media Art – GitHub Code Repository](https://github.com/NYUAD-IM/Desert-Media-Art)

## Week 8.1
- Announcements
    - Midterm grading in progress
    - Desert Site Visit - this Sunday!
        - Site scouting - find the location for your installation
        - Recommended attendance
        - Sign up at [DMA F2024 Field Trip Sign-up (Sheet)](https://docs.google.com/spreadsheets/d/1imRFU7NBYngs420RBw1VIBT79YkT-3d-Hn46mOPMQbc/edit?usp=sharing)
        - Trip details at [Desert Media Art Field Trips - Fall 2024 (Doc)](https://docs.google.com/document/d/16QtXjvqj1A35x5loTsNKnWrLmUPk_LgMrLdogXFFjx4/edit?usp=sharing)
        - Depart Welcome Center Sunday 1:30pm
        - Return Welcome Center 8pm (latest)
        - Preparation
            - Dress for the weather
            - Hat, long sleeve top, sunglasses, sandals may be ok but consider closed shoes (hot sand)
            - Sunscreen
            - Wet bandana on neck helps with the heat
            - Water bottle
            - Can bring an initial prototype
            - Can bring camera for test shooting
        - What are factors affecting the local ecology?
        - What plants and animals are living in the area?
        - Take some reference photos to use while developing your installation
        - [Filming in the Desert Tips](https://desert.nyuadim.com/2021/11/01/filming-in-the-desert-tips/)
            - Cameras / phones can overheat when filming in the sun
            - Getting proper exposure can be difficult - strong sunlight makes it easy to be overexposed

- Class Visit - Purring Tiger - MUJO
    - [Purring Tiger](https://www.purringt.com/about)
    - [Kiori Kawai](https://www.kiorikawai.com/) and [Aaron Sherwood](https://aaron-sherwood.com/)
    - [MUJO - Live Performance & Installation (Purring Tiger)](https://www.purringt.com/#/mujo/)
 
- Sensors introduction (time permitting)
    - What do you want to sense?

## Week 8.2
- Project check-in
  - Short group meeting
  - Fill in [Desert Media Art Projects](https://docs.google.com/spreadsheets/d/1iJNpbhqkyNb6HogYLb8mV5AxyQxO05a-2gKaVRbXwR4/edit?usp=sharing) with Project Name, Group Members, Inspiration, and Tech
  - What are you going to look for when we go to the desert?

- Workshop: Sensors – bring your CircuitPython kit!
    
    - Check EC2 booking system for sensors
        - [Equipment / Laser Cutter Booking](https://nyuad-artsbooking.nyu.edu/) (NYU Network/VPN Required)
            - e.g have IR range sensor available
    - Potentiometers (one of the simplest sensors – for angle)
        - [What is a potentiometer?](https://www.electrical4u.com/potentiometer/)
        - [Read potentiometer from CircuitPython](https://learn.adafruit.com/make-it-change-potentiometers/circuitpython)
    - [M4 Express Feather Pinouts](https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51/pinouts)
    - [CircuitPython Command REPL](https://learn.adafruit.com/welcome-to-circuitpython/the-repl)
        - Stop program with Command-C (sometimes)
    
    - [Photocells](https://learn.adafruit.com/photocells/overview) – resistive light sensor
        - [CircuitPython code (Adafruit)](https://learn.adafruit.com/photocells/circuitpython)
        - [CircuitPython code (photocell.py class example)](https://github.com/NYUAD-IM/Desert-Media-Art/blob/main/Code/photocell.py)
        - [Light-Activated Pixel Heart](https://learn.adafruit.com/light-activated-pixel-heart/circuitpython-code)
        - Available from IM lab parts
    
    - [Adafruit BH1750 Light Sensor](https://www.adafruit.com/product/4681) – digital light sensor
        - We have 4x available for class
    - [HC-SR04](https://www.adafruit.com/product/3942)[Ultrasonic distance sensor](https://www.adafruit.com/product/3942)
        - Mang has 2x
    - [Tutorial for touch on M4 Express](https://desert.nyuadim.com/2022/04/07/tutorial-for-touch-on-m4-express/ "Tutorial for touch on M4 Express") – make a touch sensor from metal foil
    - [Prop Maker Featherwing](https://learn.adafruit.com/adafruit-prop-maker-featherwing)
        - Built in accelerometer can [detect taps](https://learn.adafruit.com/adafruit-prop-maker-featherwing/circuitpython) and other motions like [swinging](https://learn.adafruit.com/hallowing-lightsaber/program-with-circuitpython)
    - [Soil Sensor – I2C Capacitive Moisture Sensor](https://learn.adafruit.com/adafruit-stemma-soil-sensor-i2c-capacitive-moisture-sensor)
- Workshop: LEDs (time permitting)
    - [Neopixels and 3W LED with Prop-Maker Featherwing](https://learn.adafruit.com/adafruit-prop-maker-featherwing/circuitpython)
        - You have 3W LED in kit
        - We have [rings](https://www.adafruit.com/product/1643) and [individual pixels](https://www.adafruit.com/product/4776) available for our class
        - [3W LED example code (DMA GitHub)](https://github.com/NYUAD-IM/Desert-Media-Art/blob/main/Code/bigled.py)
    - [CircuitPython NeoPixel](https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel) – general tutorial + animations, etc
- Any sensor requests?
    - [Adafruit VL53L1X Time of Flight Distance Sensor – ~30 to 4000mm](https://www.adafruit.com/product/3967) – laser distance sensor



- **Workshop**: LEDs and Servos
    - [Tutorial – NeoPixels with Prop-Maker FeatherWing](https://desert.nyuadim.com/2022/10/25/tutorial-neopixels-with-prop-maker-featherwing/)
    - [Tutorial – RGBW NeoPixels](https://desert.nyuadim.com/2022/10/26/tutorial-rgbw-neopixels/) (the small NeoPixel bar we use in class is RGBW)
    - [Tutorial for moving servo on M4 Express](https://desert.nyuadim.com/2022/04/01/tutorial-for-moving-servo-on-m4-express/)
    - [Prop-Maker FeatherWing pinouts](https://learn.adafruit.com/adafruit-prop-maker-featherwing/pinouts)
    - [Prop-Maker FeatherWing CircuitPython examples](https://learn.adafruit.com/adafruit-prop-maker-featherwing/circuitpython)
    - [FancyLED library](https://learn.adafruit.com/fancyled-library-for-circuitpython?view=all)
        - Advanced colour blending, etc
    - [3W LED example (DMA GitHub)](https://github.com/NYUAD-IM/Desert-Media-Art/blob/main/Code/bigled.py)

**3D Printing Resources**

- [Tinkercad](https://www.tinkercad.com/)
    - Online 3D design tool
    - [Learning Tinkercad](https://www.tinkercad.com/learn/designs?collectionId=OSZ5W2BL1W5N51F)
    - Tutorial example – [making a duffel button](https://www.tinkercad.com/learn/overview/OYGK7F8IYEQ4BP0?collectionId=OSZ5W2BL1W5N51F)
    - [Getting Started with 3D Printing Using Tinkercad (Sparkfun)](https://learn.sparkfun.com/tutorials/getting-started-with-3d-printing-using-tinkercad/all)

### Homework – Week 8.2

Due before Sunday

- **Get ready** for field trip
    - Water
    - Pack lunch
    - Hat, sunscreen, sunglasses
    - Think about what you want to look out for on-site as it relates to your project
        - Cellphone pictures typically have embedded GPS location, useful for finding scouted locations
    - [Gaia GPS](https://www.gaiagps.com/)
        - Can download maps for offline use
        - Can start track recording, will show path taken
        - Pictures taken while recording track can be geolocated

- **Field trip**
    - Bus leaves Welcome Center Sunday 1:30pm
    - Returning to Welcome Center 8pm (latest)

Due before start of next class

- **Start working** on Project Final Proposal (due Week 9.2 - Wednesday November 8)

---

## Desert Site Visit

### Sunday October 27

Visit site near Sweihan to see location for final installation and learn about desert ecology.

Depart Welcome Center 1:30pm

Back to campus 8pm (latest)

For full details see [Desert Media Art 2024 - Field Trips (Doc)](https://docs.google.com/document/d/16QtXjvqj1A35x5loTsNKnWrLmUPk_LgMrLdogXFFjx4/edit?usp=sharing)

- Bring water
- Bring lunch!
- Dress for the sun (hat, sunscreen)
- Closed toed shoes may be better for hot sand

---

## Week 9.1

**Field trip discussion**
Observations
- [Gaia GPS](https://www.gaiagps.com/) - offline mapping

**Project-based Production topics**

**3D Printing Resources**

- [Tinkercad](https://www.tinkercad.com/)
    - Online 3D design tool
    - [Learning Tinkercad](https://www.tinkercad.com/learn/designs?collectionId=OSZ5W2BL1W5N51F)
    - Tutorial example – [making a duffel button](https://www.tinkercad.com/learn/overview/OYGK7F8IYEQ4BP0?collectionId=OSZ5W2BL1W5N51F)
    - [Getting Started with 3D Printing Using Tinkercad (Sparkfun)](https://learn.sparkfun.com/tutorials/getting-started-with-3d-printing-using-tinkercad/all)

**Project Final Proposal Checkins**

### Homework – Week 9.1

- **Finish** your Project Final Proposal presentation and blog post
- **Prepare** an 8 minute presentation of your idea
    
    - Overview of your concept
    
    - Explanation of the interaction
    - Technical implementation
    - Conclusion / what you hot to achieve
    - Example project proposal presentation – [(We Are) Lightcatchers (pdf)](https://desert.nyuadim.com/wp-content/uploads/2022/10/Light-Catchers-Presented-at-Prototyping-Lab.key.pdf)
- **Post** your Project Proposal to the class blog – one post per group (due before next class)
    - Overview picture / sketch
    - 1 paragraph description of project (4-5 sentences)
    - 1 paragraph explaining the interaction design and how the project relates to the desert context
    - 1-2 paragraphs planned technical implementation
    - 2-3 paragraphs progress documentation
        - What you’ve tried, what you’re working on
    - 1-2 paragraphs project implementation plan
        - How you will complete the project
        - What tech you still need to implement, fabrication techniques
            - e.g. what sensors you will use, 3D printing, etc

## Week 9.2

- Project Proposal Presentations
- Workshop / Work Session: Project-based topics

### Homework – Week 9.2

Due before start of next class

- **Keep working** on your project prototyping
- **Email** any questions or problem areas with your project to the professor (one day before next class)

---

## Week 10.1
Announcments:
- Blog posts
  - Set featured image and "Fall 2023" category

- **Workshop** Project Production
- Work on projects in lab
- Consult on any problem areas

- References
  - [Sensor Plotting with Mu and CircuitPython](https://learn.adafruit.com/sensor-plotting-with-mu-and-circuitpython/capacitive-touch) - see raw touch sensor values
  - [Prop-maker Featherwing Pinouts](https://learn.adafruit.com/adafruit-prop-maker-featherwing/pinouts)
    - Note: A0 is used for audio amplifier

### Homework – Week 10.1

- **Work** on your Rapid Prototyping design

## Week 10.2

- Lecture – Requested topics
- Announcements
  - Bring USB cables to return on Monday
  - Prusa Mini is available for printing

### Homework – Week 10.2

Due before start of next class

- **Post** your storyboard on the blog - details in syllabus
  
---

## Week 11.1

Telling your story / Documenting your work / Exhibition Installation

- Documenting your work
- [How to Make a Storyboard for Video](https://photography.tutsplus.com/tutorials/how-to-make-a-storyboard-for-video--cms-26374)
- [Filming in the Desert Tips](https://desert.nyuadim.com/2021/11/01/filming-in-the-desert-tips/)
- Protecting video equipment from sand
- Introduction to Storyboard Assignment

- Exhibition Installations
- Installation examples
    - [Dune Field Modulator](https://www.michaelang.com/project/dune-field-modulator)

### Homework – Week 11.1

Due before start of next class

- **Finish** your Rapid Prototyping assignment
- **Post** your Rapid Prototyping assignment documentation to the blog (due before next class)
- **Be ready** to show your prototype in class

## Week 11.2

**Rapid Prototyping project review**

- Show your work for feedback

**Work session**

- Resolve any project issues before Field Installation

### Homework – Week 11.2

Due before start of next class

- **Finish** your Storyboard
- **Post** your Storyboard to the class blog
- **Be ready** to show your Storyboard / interaction design

---

## Week 12.1

- **Storyboard presentations** / feedback
    - Each group gets 8 minutes to present and 5 minutes feedback

- 3D printing example
    - [Neopixel Ring Diffuser (Tinkercad)](https://www.tinkercad.com/things/kf2WVfSZfiD-neopixel-ring-diffuser)
    - Using [PrusaSlicer cut tool](https://help.prusa3d.com/article/cut-tool_1779) for cutting a small test piece for printing
    
 
- Project check-in
  - 3D prints?
  - Laser cutting?
- Work session

### Homework – Week 12.1

Due before start of next class

- **Keep working** on your Prototype
- **Book** time on laser cutter, 3D printers
<!--
- **Post** your prototype status to the class blog
    
    - Photos / video of the prototype
    - Technical explanation of how it works (e.g. code, 3D designs, schematics)
    
    - What you hope to achieve in the desert
-->
- **Be ready** to show your prototype in class
- **Get ready** for the field installation!

## Week 12.2

**Work Session**

- Announcements
  - Need to book Prusa Mini before using (currently offline, will update status)
  - Ultimaker is available for booking (non-translucent materials)
  - Can ask Linda for prints in transparent material
 
- Field installation overview / planning
  - Mandatory attendance - Contact Mang immediately if can't go and not already excused

- Resolve last issues
- Get ready for the desert!

### Homework – Week 12.2

Due before start of next class

- **Be ready and packed** for the Field Installation
- **Prepare** a shot list
- **Prepare** all cameras, tripods, etc

---

# Field Installation

## Sunday November 26

## Depart Welcome Center 12:30pm – Return 9:00pm

Students will go to a “raw” (uninhabited) dune location and make a temporary installation of their class projects. The students will have approximately 2 hours to work on site before sunset, and 2 hours after sunset (total of 6 hours on site). We’ll depart from campus in a large tour bus that will park by the side of the road at the location and be our “base station” as we work in the dunes. In terms of logistics it’s similar to going out for a short film shoot in the desert.

For full details see [DMA Field Trips Doc](https://docs.google.com/document/d/1--Xma7Juj3H1Eu84iBAtigo7meBNoTOrkDTGiT0QwPo/edit?usp=sharing)

---

## Week 13.1

- Field Work Debrief
- Discussion on presenting Desert Media Art indoors
- Final Project check-in
- Final project names

### Homework – Week 13.1

Due before start of next class

- **Work** on your documentation video
- **Work** on your Final Installation and post to blog
  - **Make a sketch** or sketches of the installation
    - Overview with person for size
    - Overhead floor plan with dimensions (how much floor space you need)
  - **List** any requested equipment for your Final Installation
    - Book equipment in Connect2

## Week 13.2

- Documentation Video check-in
- Final Installation check-in
- Prepare for Final Installation
    - Space allocation
    - Final logistics / equipment organization

### Homework – Week 13.2

Due today (Dec 6)

- **Plan** on your Final Installation
  - **Make a sketch** or sketches of the installation
    - Overview with person for size
    - Overhead floor plan with dimensions (how much floor space you need)
    - Approximate sizes in cm for any plinths and tables
  - **Check** requested equipment for your Final Installation in [Projects Spreadsheet](https://docs.google.com/spreadsheets/d/1iJNpbhqkyNb6HogYLb8mV5AxyQxO05a-2gKaVRbXwR4/edit?usp=sharing)
    - Book equipment in Connect2
    - Coordinate with Scene Shop if you want to build a sandbox there
   
Due before next class
- **Work on** your Documentation Video
- **Work on** your project web page
  - Start editing your project page
    - https://desert.nyuadim.com/hekaya/
    - https://desert.nyuadim.com/desertwhispers/
    - https://desert.nyuadim.com/luminous/
    - https://desert.nyuadim.com/nomad/ 
---

## Week 14.1
- Work session – Installation, video production, web page

### Homework – Week 14.1

Due before start of next class

- **Finish** the webpage for your project on the class Wordpress
    - Written for someone seeing the project for the first time
    - Embed your project video
    - See existing projects for examples
- **Prepare** to present your project to the class (10-15 minutes)


## Week 14.2

- Final Presentations / DMA Film Festival
- Each group will present their project by giving a short “artist’s talk” / walkthrough of the project, project video, and installation
- Course review
- Preparation for IM End of Semester Show

### Homework – Week 14.2

- **Prepare** to show your project during the IM End of Semester Show
- **Take** installation photos / video of your installation during the show
- **Update** your project web page with two photos of your installation during the show

## IM Show

Friday December 15, 3-6pm

- **Exhibit** your project in the IM End of Semester Show
- **Take** photos / video of your installation in the show
- **Deinstall** your work at end of show
- **Update** your blog post with the documentation of your installation (due end of day Monday, Dec 18)


### Timeline
- Wed Dec 13 - Space setup (tables, power installed)
- Thursday Dec 14 - Black Box Desert Media Art class setup
  - Black Box busy 11-5pm for rehearsals
  - Set up and test equipment, resolve any problems
  - Luminous Rhythms - 10-11am
  - Nomad - 5-6pm
  - Hekaya - 5-7pm
  - Desert Whispers 5-7pm
  - Sand Team gets sand 5pm
      - Cart from IM lab
      - Shovel    
- Friday Dec 15 - IM End of Semester Show - 3-6pm
  - 12-2:30pm - Prayer time
  - 2:30pm - Get installation running
  - 3-5pm Installations open for viewing
    - Be ready to give a 5 minute tour at 3:30pm
        - Nomad to go last    
    - Take documentation photos
  - 5-5:45pm Performances
  - 5:45pm Closing ceremony - group picture
  - 6pm - Cleanup, return equipment to EC, help move tables
- Monday Dec 18 end of day
  - Add installation pictures / video to project webpage
- Have a great summer!
