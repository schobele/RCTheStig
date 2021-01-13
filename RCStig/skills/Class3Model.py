from .RCSkill import RCSkill

import tensorflow as tf
import numpy as np
from skimage.color import rgb2gray
from skimage import io
import skimage

#(score, diff) = compare_ssim(grayA, grayB, full=True)
#diff = (diff * 255).astype("uint8")

class Class3Model(RCSkill):

    def __init__(self, left_val, right_val, throttle, min_acc, model_path):
        self.name = "Class3Model"
        self.model = tf.keras.models.load_model(model_path)
        self.model.summary()
        self.lock = False
        self.right_val = right_val
        self.left_val = left_val
        self.straight_val = 0
        self.throttle_val = throttle
        self.min_acc = min_acc
    
    def go(self, frame):
        
        if np.random.random()>0.99:
            skimage.io.imsave("../../img_spy/example_input_in_try_loop_gray.png",frame)
        img_array = tf.keras.preprocessing.image.img_to_array(frame)
        img_array = tf.expand_dims(img_array, 0) #

        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        class_names = ['left', 'right', 'straight']
        class_vals = [self.left_val,self.right_val,self.straight_val]

        print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))

        if 100 * np.max(score) > self.min_acc:
            return {"steering": class_vals[np.argmax(score)], "gear": 1, "throttle": self.throttle_val}
        else:
            return {"steering": self.straight_val, "gear": 1, "throttle": self.throttle_val}

