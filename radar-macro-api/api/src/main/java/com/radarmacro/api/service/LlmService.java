package com.radarmacro.api.service;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.List;
import java.util.Map;

@Service
public class LlmService {

    @Value("${openai.api.key}")
    private String apiKey;

    private final String urlChat = "https://api.openai.com/v1/chat/completions";
    private final String urlEmbedding = "https://api.openai.com/v1/embeddings";

    public List<Double> gerarEmbedding(String texto) {
        Map<String, Object> requestBody = Map.of(
    "model", "text-embedding-3-small",
    "input", texto
);
    
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setBearerAuth(apiKey);

        HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);
        RestTemplate restTemplate = new RestTemplate();

        try {
            Map<String, Object> response = restTemplate.postForObject(urlEmbedding, request, Map.class);
            List<Map<String, Object>> data = (List<Map<String, Object>>) response.get("data");
            
            return (List<Double>) data.get(0).get("embedding");
            
        } catch (Exception e) {
            throw new RuntimeException("Erro ao gerar embedding na OpenAI: " + e.getMessage());
        }
    }

    public String gerarResposta(String pergunta, String contexto) {
        String promptDoSistema = "Você é o Radar Macro, um assistente financeiro especialista em economia brasileira. " +
                "Responda à pergunta do usuário baseando-se EXCLUSIVAMENTE no contexto fornecido abaixo. " +
                "Se a resposta não estiver no contexto, diga que não tem informações suficientes.\n\n" +
                "Contexto:\n" + contexto;

        Map<String, Object> requestBody = Map.of(
                "model", "gpt-4o-mini",
                "messages", List.of(
                        Map.of("role", "system", "content", promptDoSistema),
                        Map.of("role", "user", "content", pergunta)
                ),
                "temperature", 0.3
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setBearerAuth(apiKey);

        HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);
        RestTemplate restTemplate = new RestTemplate();

        try {
            Map<String, Object> response = restTemplate.postForObject(urlChat, request, Map.class);
            List<Map<String, Object>> choices = (List<Map<String, Object>>) response.get("choices");
            Map<String, Object> message = (Map<String, Object>) choices.get(0).get("message");
            return (String) message.get("content");
        } catch (Exception e) {
            return "Erro ao contatar a API da IA: " + e.getMessage();
        }
    }
}