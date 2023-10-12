<?php
/*
Plugin Name: Telegram Data Display
Description: A plugin to display data from the Telegram group using the Flask API.
Version: 1.0
Author: Your Name
*/

// Define the shortcode for displaying the data
function display_telegram_data() {
    $api_url = 'http://your-api-url/get_data';  // Replace with the actual URL of your Flask API.

    $response = wp_remote_get($api_url);

    if (is_array($response) && !is_wp_error($response)) {
        $data = json_decode($response['body'], true);
        $output = '<ul>';
        foreach ($data as $row) {
            $output .= '<li>' . esc_html($row['timestamp']) . ' - ' . esc_html($row['message']) . '</li>';
        }
        $output .= '</ul>';
    } else {
        $output = 'Error fetching data.';
    }

    return $output;
}

// Register the shortcode
add_shortcode('telegram_data', 'display_telegram_data');
