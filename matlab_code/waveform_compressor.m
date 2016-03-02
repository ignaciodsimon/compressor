function output_audio = waveform_compressor(input_audio, resolution, control_parameter, output_gain, pre_low_pass_filter_length, post_low_pass_filter_length)

    % Input low-pass filter
    filtered_input_audio = conv(input_audio, ones(pre_low_pass_filter_length, 1)/pre_low_pass_filter_length);

    % Input "hi-pass" filter
    filtered_input_audio = conv(filtered_input_audio, [1 -ones(1, 1)/1.05]);

    % Obtain gain values
    gain_values = gain(filtered_input_audio, control_parameter, resolution);

    % Obtain output
    output_audio = round(filtered_input_audio .* gain_values);

    % Output low-pass filter
    output_audio = conv(output_audio, ones(post_low_pass_filter_length, 1)/post_low_pass_filter_length) * output_gain/100;

    % Hard-limit imposed by the DAC
    for i = 1 : length(output_audio)
        if output_audio(i) > resolution/2
            output_audio(i) = resolution/2;
        end
        if output_audio(i) < -resolution/2
            output_audio(i) = -resolution/2;
        end
    end

end

function gain_value = gain(input_value, control_parameter, resolution)

    alpha = 3 / 1024 * resolution / 2;
    beta = 10 / 1024 * resolution / 2;

    exponent = alpha * control_parameter.^(control_parameter ./ resolution * 1.2);
    gain_value = (resolution + exponent) ./ (abs(input_value) + exponent + beta);

end
