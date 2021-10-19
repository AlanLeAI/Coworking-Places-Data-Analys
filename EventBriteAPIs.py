from eventbrite import Eventbrite

eventbrite = Eventbrite('TF74N3BCQZ5HD5QWQIOY')

user = eventbrite.get_user()

event = eventbrite.get_event('12345')

print(event)
