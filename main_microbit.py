def on_data_received():
    global cmd
    cmd = serial.read_until(serial.delimiters(Delimiters.HASH))
    if cmd == "0":
        radio.send_value("LED", 0)
    elif cmd == "1":
        radio.send_value("LED", 1)
    elif cmd == "2":
        radio.send_value("FAN", 2)
    elif cmd == "3":
        radio.send_value("FAN", 3)


serial.on_data_received(serial.delimiters(Delimiters.HASH), on_data_received)


def on_received_value(name, value):
    serial.write_string("!1:" + name + ":" + ("" + str(value)) + "#")
    basic.show_string(name)
    basic.show_number(value)


radio.on_received_value(on_received_value)

cmd = ""
radio.set_group(231)
