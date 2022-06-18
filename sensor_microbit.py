def on_received_value(name, value):
    if name == "LED":
        if value == 0:
            basic.show_icon(IconNames.HEART)
        elif value == 1:
            basic.show_icon(IconNames.SMALL_HEART)
    elif name == "FAN":
        if value == 2:
            basic.show_icon(IconNames.SQUARE)
        elif value == 3:
            basic.show_icon(IconNames.SMALL_SQUARE)
radio.on_received_value(on_received_value)

radio.set_group(231)
count = 10

def on_forever():
    global count
    if count == 10:
        radio.send_value("TEMP", input.temperature())
    elif count == 5:
        radio.send_value("LIGHT", input.light_level())
    elif count == 0:
        count = 10
    basic.pause(1000)
    count += -1
basic.forever(on_forever)
