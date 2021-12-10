#!/usr/bin/python37all
import cgi
import json
data = cgi.FieldStorage()
sounds = data.getvalue('sounds') 
mhours = data.getvalue('mhours') 
nhours = data.getvalue('nhours') 
rhours = data.getvalue('rhours') 
mmin = data.getvalue('mmin') 
nmin = data.getvalue('nmin') 
rmin = data.getvalue('rmin') 
mtime = data.getvalue('mtime')
ntime = data.getvalue('ntime') 
rtime = data.getvalue('rtime') 
test = data.getvalue('test')
snooze = data.getvalue('snooze')
###import calendar data potentially to display dates
web = {"sounds":sounds, "mhours":mhours, "nhours":nhours, "rhours":rhours, "mmin":mmin, "nmin":nmin, "rmin":rmin, "mtime":mtime, "ntime":ntime, "rtime":rtime, "test":test, "snooze":snooze}
with open('final.txt', 'w') as f:
  json.dump(web,f) 

print('Content-type:text/html\n\n')
print('<html>')
print('<div>')
print('<div style="width: 1200px; background: #40E0D0; border: 1px; text-align: center;"><br />')
print('<h2>ENME441 Smart Alarm</h2>')
print('<p style="font-size: 1.5em;"><strong>Input in your preferences</strong></p>')
print('<div style="width: 1200px; background: #b0e0e6; border: 2px; text-align: center;"><br />')
print('<form action="/cgi-bin/finalproject.py" method="POST">')
print('<label for="sounds">Choose Sound: </label><select id="sounds" name="sounds">')
print('<option value="sound1">Sound 1</option>')
print('<option value="sound2">Sound 2</option>')
print('<option value="sound3">Sound 3</option>')
print('<option value="sound4">Sound 4</option>')
print('</select>')
print('<input type="radio" name="test" value="testing" > Test Sound')
print('<input type="radio" name="test" value="change"> Change Sound <br>')
print('<br />Number of Snoozes :')
print('<select name="snooze">')
print('<option value="0">0</option>')
print('<option value="1">1</option>')
print('<option value="2">2</option>')
print('<option value="3">3</option>')'
print('</select>')
print('<br /><br />How Early to Wake Up Before Event:<select name="mhours">')
print('<option value="0">0</option>')
print('<option value="1">1</option>')
print('<option value="1">1</option>')
print('<option value="2">2</option>')
print('<option value="3">3</option>')
print('<option value="4">4</option>')
print('<option value="5">5</option>')
print('<option value="6">6</option>')
print('<option value="7">7</option>')
print('<option value="8">8</option>')
print('<option value="9">9</option>')
print('<option value="10">10</option>')
print('<option value="11">11</option>')
print('<option value="12">12</option>')
print('<option value="13">13</option>')
print('<option value="14">14</option>')
print('<option value="15">15</option>')
print('<option value="16">16</option>')
print('<option value="17">17</option>')
print('<option value="18">18</option>')
print('<option value="19">19</option>')
print('<option value="20">20</option>')
print('<option value="21">21</option>')
print('<option value="22">22</option>')
print('<option value="23">23</option>')
print('</select><select name="mmin">')
print('<option value="0">0</option>')
print('<option value="15">15</option>')
print('<option value="30">30</option>')
print('<option value="45">45</option>')
print('</select>')
print('<br /><br />When to set the bedtime alarm:<select name="nhours">')
print('<option value="0">0</option>')
print('<option value="1">1</option>')
print('<option value="1">1</option>')
print('<option value="2">2</option>')
print('<option value="3">3</option>')
print('<option value="4">4</option>')
print('<option value="5">5</option>')
print('<option value="6">6</option>')
print('<option value="7">7</option>')
print('<option value="8">8</option>')
print('<option value="9">9</option>')
print('<option value="10">10</option>')
print('<option value="11">11</option>')
print('<option value="12">12</option>')
print('<option value="13">13</option>')
print('<option value="14">14</option>')
print('<option value="15">15</option>')
print('<option value="16">16</option>')
print('<option value="17">17</option>')
print('<option value="18">18</option>')
print('<option value="19">19</option>')
print('<option value="20">20</option>')
print('<option value="21">21</option>')
print('<option value="22">22</option>')
print('<option value="23">23</option>')
print('</select><select name="nmin">')
print('<option value="0">0</option>')
print('<option value="15">15</option>')
print('<option value="30">30</option>')
print('<option value="45">45</option>')
print('</select>')
print('<br /><br />When to Refresh:<select name="rhours">')
print('<option value="0">0</option>')
print('<option value="1">1</option>')
print('<option value="1">1</option>')
print('<option value="2">2</option>')
print('<option value="3">3</option>')
print('<option value="4">4</option>')
print('<option value="5">5</option>')
print('<option value="6">6</option>')
print('<option value="7">7</option>')
print('<option value="8">8</option>')
print('<option value="9">9</option>')
print('<option value="10">10</option>')
print('<option value="11">11</option>')
print('<option value="12">12</option>')
print('<option value="13">13</option>')
print('<option value="14">14</option>')
print('<option value="15">15</option>')
print('<option value="16">16</option>')
print('<option value="17">17</option>')
print('<option value="18">18</option>')
print('<option value="19">19</option>')
print('<option value="20">20</option>')
print('<option value="21">21</option>')
print('<option value="22">22</option>')
print('<option value="23">23</option>')
print('</select><select name="rmin">')
print('<option value="0">0</option>')
print('<option value="15">15</option>')
print('<option value="30">30</option>')
print('<option value="45">45</option>')
print('</select>')
print('<br /><br /><input type="submit" value="Submit Changes" />')
print('</form>')
print('Current Wake UP Alarm is: %s:%s ' % (mhours,mmin))
print('Before Event')
print('<br />')
print('Current Sleep Alarm is: %s:%s ' % (nhours,nmin))
print('Before Event')
print('<br />')
print('Current Refresh Time is: %s:%s ' % (rhours,rmin))
print('Before Event')
print('<br />')
print('</div>')
print('</div>')
print('</div>')
print('</html>')