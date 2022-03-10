# rotary_encoder
Reading input form a rotary encoder with an implementation of John Main's software debouncing explain here: https://www.best-microcontroller-projects.com/rotary-encoder.html

The idea is to filter inputs through a table of physicaly "legal" moves and ignore input combinations that cannot come from normal operation (i.e., inputs combinations that arise from bouncing).

