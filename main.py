import os
import time
import glob
import logging
import traceback
import asyncio
import signal
import numpy as np
import zmq
from zmq.asyncio import Context

from commons.common_zmq import recv_array_with_json, initialize_subscriber, initialize_publisher
from commons.configuration_manager import ConfigurationManager
from commons.car_controls import CarControlUpdates

import skimage
import skimage.transform
from skimage import io

from RCStig.RCStig import RCStig

async def main_worker(context: Context):
    config_manager = ConfigurationManager()
    conf = config_manager.config

    data_queue = context.socket(zmq.SUB)
    controls_queue = context.socket(zmq.PUB)

    rc_stig = RCStig('rcstig', 'race')

    try:
        print("try")
        await initialize_subscriber(data_queue, conf.data_queue_port)
        await initialize_publisher(controls_queue, conf.controls_queue_port)

        while True:
            frame, data = await recv_array_with_json(queue=data_queue)
            frame = frame[:,::-1,:] 
                        
            if np.random.random()>0.99:
                skimage.io.imsave("./img_spy/example_input_in_try_loop.png",frame)

            if frame is None:
                # Send back these first few instances, as the other application expects 1:1 responses
                print("NONE NONE NONE NONE")
                controls_queue.send_json({'d_steering':0,'d_gear':1,'d_throttle':0}) #TODO need to send repetition of last command or {'d_steer':0,....}
                continue

            try:

                rc_stig.act(frame)
                c = rc_stig.getControls()
                controls = {'d_steering':c["steering"],'d_gear':c["gear"],'d_throttle':c["throttle"]}
                controls_queue.send_json(controls)

            except Exception as ex:
                print("Predicting exception: {}".format(ex))
                traceback.print_tb(ex.__traceback__)
    except Exception as ex:
        print("Exception: {}".format(ex))
        traceback.print_tb(ex.__traceback__)
    finally:
        data_queue.close()
        controls_queue.close()

def signal_cancel_tasks(loop):
    loop = asyncio.get_event_loop()
    for task in asyncio.Task.all_tasks(loop):
        task.cancel()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    loop = asyncio.get_event_loop()
    #loop.add_signal_handler(signal.SIGINT, cancel_tasks, loop)
    #loop.add_signal_handler(signal.SIGTERM, cancel_tasks, loop)
    signal.signal(signal.SIGINT, signal_cancel_tasks)
    signal.signal(signal.SIGTERM, signal_cancel_tasks)
    context = zmq.asyncio.Context()
    try:
        loop.run_until_complete(main_worker(context))
    except Exception as ex:
        logging.error("Base interruption: {}".format(ex))
        traceback.print_tb(ex.__traceback__)
    finally:
        loop.close()
        context.destroy()
