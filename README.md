# DECAURA/DECADENCIA

## Purpose

Installation for Mostra Sonora i Audiovisual - Convent de Sant Agusti, 2023 - Barcelona.

By Rebecca Anne Peters and Óscar González.

## Usage

1. Launch `sonic-pi` on a raspberry pi with `startsp.sh`. This is for using sonic-pi without a screen.

2. Use [sonic-pi-tool](https://github.com/oscgonfer/sonic-pi-tool) (forked from [emlyn](https://github.com/emlyn/sonic-pi-tool) to interact with sonic-pi server from the command line. You can run a composition with `sonic-pi-tool.py run-file <composition>`

3. Install python requirements (python 3 only). 

4. We use [this adafruit DAC](https://learn.adafruit.com/adafruit-i2s-audio-bonnet-for-raspberry-pi) with a Pi-zero. With this we output to a speaker. We also use one `GPIO` (`17`) from the pi to control some lights with relays - this control is done with `osc` messages from sonic-pi that are listened by `async.py`. Modify `SERVER_IP`, `SERVER_PORT`and `UDP_FILTER` accordingly to listen to your `osc` messages.

5. `controller.py` is a simple random player using calls to `sonic-pi-tool`. It also checks everything is fine on the server side at boot. We use it with a cronjob `@reboot`, alongside `startsp.sh` to spin a server without a screen on a pi zero

That's it!
