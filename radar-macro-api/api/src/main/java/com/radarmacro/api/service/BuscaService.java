package com.radarmacro.api.service;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;
import java.time.LocalDate;

@Service
public class BuscaService {

    private final JdbcTemplate db;

    public BuscaService(JdbcTemplate db) {
        this.db = db;
    }

    public List<Map<String, Object>> buscarTrechosHibridos(String dataCorte, List<Double> vetorPergunta) {
        
        String sql = """
            SELECT conteudo, data_publicacao, fonte, tipo_documento 
            FROM documentos_copom 
            WHERE data_publicacao >= ?
            ORDER BY embedding <=> ?::vector 
            LIMIT 3;
        """;

        LocalDate dataFiltro = LocalDate.parse(dataCorte);
        
        String vetorFormatado = vetorPergunta.toString();
        
        return db.queryForList(sql, dataFiltro, vetorFormatado);
    }
}