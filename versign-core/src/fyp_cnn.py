#!/usr/bin/env python
"""sigver_cnn.py: Implementation of the Convolutional Neural Network used in
'Learning features for offline handwritten signature verification using deep
convolutional neural networks'.

Model can be trained and saved using this script."""

__author__      = "Muhammad Mahad Tariq"
__credits__ = ["Hafemann", "Robert Sabourin", "Oliveira"]
__status__ = "Development"

import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)

def cnn_model_fn(features, labels, mode):
  """Model function for CNN."""
  # Input Layer
  input_layer = tf.reshape(features["x"], [-1, 150, 220, 1])

  # Output Tensor Shape is calculated as follows:
  #     Width -> (InputWidth−FilterWidth+2Padding)/Stride+1
  #     Height -> (InputHeight−FilterHeight+2Padding)/Stride+1
  #     Depth -> No. of Filters

  # Convolutional Layer #1
  # Input Tensor Shape: [batch_size, 150, 220, 1]
  # Output Tensor Shape: [batch_size, 37, 53, 96]
  conv1 = tf.layers.conv2d(
      inputs=input_layer,
      filters=96,
      strides=4,
      kernel_size=[11, 11],
      padding="valid",
      activation=tf.nn.relu)

  # Pooling Layer #1
  # Input Tensor Shape: [batch_size, 37, 53, 96]
  # Output Tensor Shape: [batch_size, 18, 26, 96]
  pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[3, 3], strides=2)

  # Convolutional Layer #2
  # Input Tensor Shape: [batch_size, 18, 26, 96]
  # Output Tensor Shape: [batch_size, 18, 26, 256]
  conv2 = tf.layers.conv2d(
      inputs=pool1,
      filters=256,
      kernel_size=[5, 5],
      strides=1,
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #2
  # Input Tensor Shape: [batch_size, 18, 26, 256]
  # Output Tensor Shape: [batch_size, 8, 12, 256]
  pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[3, 3], strides=2)

  # Convolution Layer #3
  # Input Tensor Shape: [batch_size, 8, 12, 256]
  # Output Tensor Shape: [batch_size, 8, 12, 384]
  conv3 = tf.layers.conv2d(
    inputs=pool2,
    filters=384,
    kernel_size=[3, 3],
    strides=1,
    padding="same",
    activation=tf.nn.relu)

  # Convolution Layer #4
  # Input Tensor Shape: [batch_size, 8, 12, 384]
  # Output Tensor Shape: [batch_size, 8, 12, 384]
  conv4 = tf.layers.conv2d(
    inputs=conv3,
    filters=384,
    kernel_size=[3, 3],
    strides=1,
    padding="same",
    activation=tf.nn.relu)

  # Convolution Layer #5
  # Input Tensor Shape: [batch_size, 8, 12, 384]
  # Output Tensor Shape: [batch_size, 8, 12, 384]
  conv5 = tf.layers.conv2d(
    inputs=conv4,
    filters=384,
    kernel_size=[3, 3],
    strides=1,
    padding="same",
    activation=tf.nn.relu)

  # Convolution Layer #6
  # Input Tensor Shape: [batch_size, 8, 12, 384]
  # Output Tensor Shape: [batch_size, 8, 12, 256]
  conv6 = tf.layers.conv2d(
    inputs=conv5,
    filters=256,
    kernel_size=[3, 3],
    strides=1,
    padding="same",
    activation=tf.nn.relu)

  # Pooling Layer #3
  # Input Tensor Shape: [batch_size, 8, 12, 256]
  # Output Tensor Shape: [batch_size, 3, 5, 256]
  pool3 = tf.layers.max_pooling2d(
      inputs=conv6,
      pool_size=[3, 3],
      strides=2)

  # Flatten tensor into a batch of vectors
  # Input Tensor Shape: [batch_size, 3, 5, 256]
  # Output Tensor Shape: [batch_size, 3 * 5 * 256]
  pool2_flat = tf.reshape(pool2, [-1, 256 * 3 * 5])

  # Dense Layer
  # Densely connected layer with 2048 neurons
  # Input Tensor Shape: [batch_size, 3 * 5 * 256]
  # Output Tensor Shape: [batch_size, 2048]
  dense1 = tf.layers.dense(inputs=pool2_flat, units=2048, activation=tf.nn.relu)
  dense2 = tf.layers.dense(inputs=dense1, units=2048, activation=tf.nn.relu)

  # Add dropout operation; 0.6 probability that element will be kept
  dropout = tf.layers.dropout(
      inputs=dense2, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

  # Logits layer
  # Input Tensor Shape: [batch_size, 2048]
  # Output Tensor Shape: [batch_size, 531]
  logits = tf.layers.dense(inputs=dropout, units=531)

  predictions = {
      # Generate predictions (for PREDICT and EVAL mode)
      "classes": tf.argmax(input=logits, axis=1),
      # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
      # `logging_hook`.
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
  }
  if mode == tf.estimator.ModeKeys.PREDICT:
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

  # Calculate Loss (for both TRAIN and EVAL modes)
  loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

  # Here we use tf.train.momentumOptimizer with nestrov = true
  # Configure the Training Op (for TRAIN mode)
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.MomentumOptimizer(
        momentum=0.9,
        learning_rate=10e-3,
        use_nesterov=True)
    train_op = optimizer.minimize(
        loss=loss,
        global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

  # Add evaluation metrics (for EVAL mode)
  eval_metric_ops = {
      "accuracy": tf.metrics.accuracy(
          labels=labels, predictions=predictions["classes"])}
  return tf.estimator.EstimatorSpec(
      mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)

def main(unused_argv):
  # Load training and eval data
  mnist = tf.contrib.learn.datasets.load_dataset("mnist")
  train_data = mnist.train.images  # Returns np.array
  train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
  eval_data = mnist.test.images  # Returns np.array
  eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

  print train_data.shape, eval_data.shape, eval_labels.shape
  exit(0)

  # Create the Estimator
  mnist_classifier = tf.estimator.Estimator(
      model_fn=cnn_model_fn, model_dir="/tmp/mnist_convnet_model")

  # Set up logging for predictions
  # Log the values in the "Softmax" tensor with label "probabilities"
  tensors_to_log = {"probabilities": "softmax_tensor"}
  logging_hook = tf.train.LoggingTensorHook(
      tensors=tensors_to_log, every_n_iter=50)

  # Train the model
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": train_data},
      y=train_labels,
      batch_size=32,#
      num_epochs=60,#
      shuffle=True)
  mnist_classifier.train(
      input_fn=train_input_fn,
      steps=20000,
      hooks=[logging_hook])

  # Evaluate the model and print results
  eval_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": eval_data},
      y=eval_labels,
      num_epochs=1,
      shuffle=False)
  eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
  print eval_results


if __name__ == "__main__":
  tf.app.run()
