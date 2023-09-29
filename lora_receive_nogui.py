#!/usr/bin/env python2

import lora
import osmosdr
from gnuradio import gr
from gnuradio import blocks
from lora.loraconfig import LoRaConfig
import time


class lora_receive_nogui(gr.top_block):
    def __init__(
        self,
        udp_sink_host,
        sample_rate=1000000,
        center_freq=915000000,
        bandwidth=125000,
        spreading_factor=7,
        coding_rate=1,
    ):
        gr.top_block.__init__(self, "Lora Receive, No GUI")

        self.decimation = 1

        ##################################################
        # Blocks
        ##################################################
        self.message_socket_sink_0 = lora.message_socket_sink(udp_sink_host, 40868, 0)
        self.rtlsdr_source_0 = osmosdr.source()
        self.rtlsdr_source_0.set_sample_rate(sample_rate)
        self.rtlsdr_source_0.set_center_freq(center_freq, 0)
        self.lora_receiver_0 = lora.lora_receiver(
            samp_rate=sample_rate,
            center_freq=center_freq,
            channel_list=[center_freq],
            bandwidth=bandwidth,
            sf=spreading_factor,
            implicit=False,
            cr=coding_rate,
            crc=True,
        )
        self.blocks_throttle = blocks.throttle(gr.sizeof_gr_complex, sample_rate, True)


        ##################################################
        # Connections
        ##################################################
        # self.connect((self.blocks_throttle, 0), (self.rtlsdr_source_0, 0))
        self.msg_connect((self.lora_receiver_0, 'frames'), (self.message_socket_sink_0, 'in'))
        self.connect((self.rtlsdr_source_0, 0), (self.lora_receiver_0, 0))

def main(udp_sink_host):
    tb = lora_receive_nogui(udp_sink_host)
    tb.start()
    # tb.wait()
    time.sleep(10)
    tb.stop()

if __name__ == "__main__":
    main("127.0.0.1")
