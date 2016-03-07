% This script tests the two operating methods of the compressor: based on a
% sample and based on a frame of samples.
%
% Both methods are applied in cascade. The result is a nice, compressed and
% lightly saturated signal. It can also offer very compressed and saturated
% sounds.
%
% Joe.

audio_filename = 'guitar_clean.wav';

resolution = 2^12;  % = 4096

% Frame compression controls
frame_compression_enabled = 1;
frame_control_parameter = 1000;%1400;
frame_window_size = 500;
frame_output_gain = 15;

% Waveform compression controls
waveform_compression_enabled = 1;
waveform_control_parameter_hi = 1200; %60;   % <-- Use these controls to make
waveform_control_parameter_lo = 1200; %3000; %     the distortion asymmetrical
waveform_output_gain = 20;
waveform_pre_low_pass_filter_length = 20;
waveform_post_low_pass_filter_length = 4;

% -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

% Load input audio
[input_audio, sample_rate] = audioread(audio_filename);

% input_audio = sin(2*pi*1000/48000 * [0:48000]);

% Normalise input audio to discrete range
input_audio = round(input_audio / max(abs(input_audio)) * resolution / 2);

processed_audio = input_audio;

% Frame compression
if frame_compression_enabled
    processed_audio = frame_compressor(processed_audio, resolution, frame_control_parameter, ...
                                    frame_window_size, frame_output_gain);
end

% Waveform compression
if waveform_compression_enabled
    processed_audio = waveform_compressor(processed_audio, resolution, waveform_control_parameter_hi, ...
                                       waveform_control_parameter_lo, ...
                                       waveform_output_gain, waveform_pre_low_pass_filter_length, ...
                                       waveform_post_low_pass_filter_length);
end

% Denormalise input / output audios
input_audio = input_audio / max(abs(input_audio));
output_audio = processed_audio / max(abs(processed_audio));

% Save processed audio to file
audiowrite(sprintf('%s_processed.wav', audio_filename), output_audio, sample_rate);

% -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

subplot(2,1,1)
plot(input_audio)
% xlim([60000 61000])
xlim([10000 11000])
grid
title('Input audio')
subplot(2,1,2)
plot(output_audio)
% xlim([60000 61000])
xlim([10000 11000])
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
