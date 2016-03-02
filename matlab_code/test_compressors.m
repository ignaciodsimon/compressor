% This script tests the two operating methods of the compressor: based on a
% sample and based on a frame of samples.
%
% Both methods are applied in cascade. The result is a nice, compressed and
% lightly saturated signal.
%
% Joe.

audio_filename = 'bass_clean.wav';

resolution = 2^12;  % = 4096

% Frame compression controls
frame_control_parameter = 1400;
frame_window_size = 400;
frame_output_gain = 15;

% Waveform compression controls
waveform_control_parameter = 600;
waveform_output_gain = 20;
waveform_pre_low_pass_filter_length = 20;
waveform_post_low_pass_filter_length = 4;

% -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

% Load input audio
[input_audio, sample_rate] = audioread(audio_filename);

% Normalise input audio to discrete range
input_audio = round(input_audio / max(abs(input_audio)) * resolution / 2);

% Waveform compression
output_audio = waveform_compressor(input_audio, resolution, waveform_control_parameter, ...
                                   waveform_output_gain, waveform_pre_low_pass_filter_length, ...
                                   waveform_post_low_pass_filter_length);

% Frame compression
output_audio = frame_compressor(output_audio, resolution, frame_control_parameter, ...
                                frame_window_size, frame_output_gain);

% Denormalise input / output audios
input_audio = input_audio / max(abs(input_audio));
output_audio = output_audio / max(abs(output_audio));

% Save processed audio to file
audiowrite(sprintf('%s_processed.wav', audio_filename), output_audio, sample_rate);

% -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

subplot(2,1,1)
plot(input_audio)
grid
title('Input audio')
subplot(2,1,2)
plot(output_audio)
grid
title('Output audio')
% return

p = audioplayer(input_audio, sample_rate);
disp('Input signal. Press enter to continue ...');
play(p)
pause
stop(p)
p = audioplayer(output_audio, sample_rate);
play(p)
disp('Press enter to finish ...');
pause
stop(p)
close all
