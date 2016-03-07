function output_audio = frame_compressor(input_audio, resolution, frame_control_parameter, frame_window_size, frame_output_gain)

    did_peak_times = 0;
    output_audio = zeros(size(input_audio));

    for i = 1 + frame_window_size: length(input_audio)

        % For a rectangular, displacing window
        current_average = sqrt( sum(input_audio(i-frame_window_size : i).^2) / frame_window_size);
        current_gain = gain(current_average, frame_control_parameter, resolution);

        % Simulation of the hard-limit imposed by the DAC
        current_output = round(input_audio(i-frame_window_size) * current_gain * frame_output_gain/100);
        if current_output > resolution/2
            current_output = resolution/2;
            did_peak_times = did_peak_times + 1;
        end
        if current_output < -resolution/2
            current_output = -resolution/2;
            did_peak_times = did_peak_times + 1;
        end
        output_audio(i-frame_window_size) = current_output;
    end

    if did_peak_times
        disp(sprintf('[Warning] The output signal of the FRAME compressor peaked for: %d [samples]', did_peak_times))
    end
end

function gain_value = gain(input_value, control_parameter, resolution)

    alpha = 3 / 1024 * resolution / 2;
    beta = 10 / 1024 * resolution / 2;

    exponent = alpha * control_parameter.^(control_parameter ./ resolution * 1.2);
    gain_value = (resolution + exponent) ./ (abs(input_value) + exponent + beta);

end
