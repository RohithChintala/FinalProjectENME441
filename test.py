currenthour = 1
nighth = 1
currentminute = 1
nightm = 1

morningh = 2
morningm = 2

if int(currenthour) == int(nighth):
  if int(currentminute) == int(nightm):
    print('nightalarm') ###where alarm goes
    write(5, 0, '%s:%s' % (currenthour,currentminute))
    write(2, 1, 'Time To Sleep')
    buzzsetup()
    buzzloop()
    if GPIO.input(buttonPin) == 1:
      buzzdestroy()
      write(0, 1, 'Alarm Off')
    
if int(currenthour) == int(morningh):
  if int(currentminute) == int(morningm):
    print('dayalarm')  ###where alarm goes
    write(5, 0, '%s:%s' % (currenthour,currentminute))
    write(2, 1, 'Wake Up')
    buzzsetup()
    buzzloop()
    if GPIO.input(buttonPin) == 1:
      buzzdestroy()
      write(0, 1, 'Alarm Off')