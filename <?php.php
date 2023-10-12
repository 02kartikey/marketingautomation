<?php
/*
Plugin Name: Telegram Data Display
Description: A WordPress plugin to display data from the Telegram group using a Flask API.
Version: 1.0
Author: Your Name
*/

// Define the shortcode for displaying the data
function telegram_data_shortcode() {
    $api_url = 'http://your-api-url/get_data';  // Replace with the actual URL of your Flask API.

    $response = wp_remote_get($api_url);

    if (is_wp_error($response)) {
        return 'Error: API request failed.';
    }

    $http_code = wp_remote_retrieve_response_code($response);

    if ($http_code !== 200) {
        return 'Error: API returned a non-200 status code.';
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    if (is_array($data)) {
        $output = '<ul>';
        foreach ($data as $row) {
            $output .= '<li>' . esc_html($row['timestamp']) . ' - ' . esc_html($row['message']) . '</li>';
        }
        $output .= '</ul>';
    } else {
        $output = 'Error: Data format is not as expected.';
    }

    return $output;
}

// Register the shortcode
add_shortcode('telegram_data', 'telegram_data_shortcode');