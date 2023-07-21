package WebClientObserver;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
public class SmartFactoryClient {
    private static JLabel ipAddressLabel;
    private static JLabel temperatureLabel;
    private static JLabel photoresistorLabel;
    private static JLabel countLabel;
    public static void main(String[] args) {
        JFrame frame = new JFrame("HyeonJin Smart Factory");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 400);
        frame.setLayout(new BorderLayout());

        JPanel mainPanel = new JPanel(new GridLayout(4, 1));
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER));

        ipAddressLabel = new JLabel("IP Address: ");
        temperatureLabel = new JLabel("Temperature: ");
        photoresistorLabel = new JLabel("Photoresistor Value: ");
        countLabel = new JLabel("Object Count: ");

        Font labelFont = new Font("Arial", Font.PLAIN, 20); // Increase font size
        ipAddressLabel.setFont(labelFont);
        temperatureLabel.setFont(labelFont);
        photoresistorLabel.setFont(labelFont);
        countLabel.setFont(labelFont);

        JButton refreshButton = new JButton("Check Condition");
        refreshButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                updateLabels();
            }
        });

        buttonPanel.add(refreshButton);
        mainPanel.add(ipAddressLabel);
        mainPanel.add(temperatureLabel);
        mainPanel.add(photoresistorLabel);
        mainPanel.add(countLabel);

        frame.add(mainPanel, BorderLayout.CENTER);
        frame.add(buttonPanel, BorderLayout.SOUTH);
        frame.setVisible(true);
    }

    private static void updateLabels() {
        String urlStr = "http://192.168.15.110:80/"; // Update with your server's IP address
        try {
            URL url = new URL(urlStr);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String line;
                while ((line = reader.readLine()) != null) {
                    if (line.contains("Temperature:")) {
                        temperatureLabel.setText(line);
                    } else if (line.contains("Photoresistor Value:")) {
                        photoresistorLabel.setText(line);
                    } else if (line.contains("Object Count:")) {
                        countLabel.setText(line);
                    } else if (line.contains("Your IP address:")) {
                        ipAddressLabel.setText(line);
                    }
                }
                reader.close();
            } else {
                JOptionPane.showMessageDialog(null, "Http connection failed : " + responseCode);
            }
            connection.disconnect();
        } catch (IOException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(null, "Exception occurred." + e.getMessage());
        }
    }
}