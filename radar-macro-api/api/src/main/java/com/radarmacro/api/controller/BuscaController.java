package com.radarmacro.api.controller;
import com.radarmacro.api.service.BuscaService;
import com.radarmacro.api.service.LlmService;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/rag")
public class BuscaController {

    private final BuscaService buscaService;
    private final LlmService llmService;

    public BuscaController(BuscaService buscaService, LlmService llmService) {
        this.buscaService = buscaService;
        this.llmService = llmService;
    }

    public record PerguntaDTO(String pergunta) {}

    public record RespostaDTO(String respostaGerada, List<Map<String, Object>> fontes) {}

    @PostMapping("/perguntar")
    public RespostaDTO fazerPergunta(@RequestBody PerguntaDTO dados) {
        String dataCorte = "2024-01-01";
        
        List<Double> vetorPergunta = llmService.gerarEmbedding(dados.pergunta());
        
        List<Map<String, Object>> trechosRelevantes = buscaService.buscarTrechosHibridos(dataCorte, vetorPergunta);
        
        StringBuilder contexto = new StringBuilder();
        for (Map<String, Object> trecho : trechosRelevantes) {
            contexto.append(trecho.get("conteudo")).append("\n\n");
        }
        
        String respostaFinal = llmService.gerarResposta(dados.pergunta(), contexto.toString());
        
        return new RespostaDTO(respostaFinal, trechosRelevantes);
    }
}