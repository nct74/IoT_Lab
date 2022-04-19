def on_data_received():
    global cmd
    cmd = serial.read_until(serial.delimiters(Delimiters.HASH))
    # basic.show_string(cmd)
    if cmd == "0":
        basic.show_icon(IconNames.SAD)
    elif cmd == "1":
        basic.show_icon(IconNames.HAPPY)
    elif cmd == "2":
        basic.show_icon(IconNames.SMALL_HEART)
    elif cmd == "3":
        basic.show_icon(IconNames.HEART)


serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)

cmd = ""
count = 5


def on_forever():
    global count
    if count == 10:
        serial.write_string("!1:TEMP:" + ("" + str(input.temperature())) + "#")
    if count == 5:
        serial.write_string("!1:LIGHT:" + ("" + str(input.light_level())) + "#")
    count += -1
    if count == 0:
        count = 5
    basic.pause(1000)


basic.forever(on_forever)
