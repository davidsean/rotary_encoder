# rotary_encoder
Reading input form a rotary encoder with software debouncing trick found in https://www.best-microcontroller-projects.com/rotary-encoder.html

The idea is to filter inpouts through a table of physicaly "legal" moves and ignore input combinations that cannot come from normal operation (i.e., arise from bouncing).

