import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class SmartFactoryClient {
    public static void main(String[] args) {
        String urlStr = "http://192.168.15.110:80";

        try {
            URL url = new URL(urlStr);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET"); // ctrl + b 통해 함수내용 확인가능

            int responseCode = connection.getResponseCode();    // status code
            //if(responseCode == 200)
            if(responseCode == HttpURLConnection.HTTP_OK){
                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
                while((line = reader.readLine()) != null){
                    response.append(line);
                    response.append('\n');
                }
                reader.close(); // buffer closed

                String[] lines = response.toString().split("\n");
                if(lines.length >= 4){
                    String ipLine = lines[2];
                    String temperatureLine = lines[3];
                    String ip_address = ipLine.split(": ")[1];
                    String temperature = temperatureLine.split(": ")[1];

                    System.out.println("IP address: " + ip_address);
                    System.out.println("온도 : " + temperature);
                    //System.out.println(lines[3]);
                }else{
                    System.out.println("Response format error!");
                }
            }else{
                System.out.println("Http connection failed: " + responseCode);
            }
            connection.disconnect();
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
