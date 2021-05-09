package com.teste.vacas.vacas.controller;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import javax.transaction.Transactional;
import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.teste.vacas.vacas.modelo.Vaca;
import com.teste.vacas.vacas.modelo.dto.VacaDto;
import com.teste.vacas.vacas.repository.VacasRepository;
import com.teste.vacas.vacas.validacaoconfig.DataEcxeption;
import com.teste.vacas.vacas.validacaoconfig.NumeroEcxeption;
import com.teste.vacas.vacas.validacaoconfig.VacaEcxeption;

@RestController
@RequestMapping("/vacas")
public class VacasController {

	private static DateTimeFormatter formater = DateTimeFormatter.ofPattern("dd-MM-yyyy");
	// private static DateTimeFormatter formaterBr =
	// DateTimeFormatter.ofPattern("dd-MM-yyyy")
	// .withLocale(new Locale("pt", "BR"));
	@Autowired
	private VacasRepository vacasRepository;

	private final List<String> cores = Arrays.asList("amarelo", "verde", "branco", "cinza", "vermelho");

	@GetMapping
	public List<VacaDto> buscarVacas(@RequestParam(required = false) Optional<String> cor) {
		List<Vaca> vacas = vacasRepository.findAllByOrderByNome();
		if (cor.isEmpty() || corExiste(cor)) {
			return VacaDto.converter(vacas.stream().map(v -> {
				v.setCor(setCor(v));
				return v;
			}).collect(Collectors.toList()));
		}
		return VacaDto.converter(vacas.stream().map(v -> {
			v.setCor(setCor(v));
			return v;
		}).filter(x -> x.getCor().equals(cor.get())).collect(Collectors.toList()));
	}

	@GetMapping("/pesquisa")
	public List<VacaDto> pesquisaVacas(@RequestParam(required = false) String str) {
		String data = str;
		if (data.length() < 10) {
			data = "01-01-1971";
		}
		List<Vaca> vacas = vacasRepository
				.findByNomeIgnoreCaseContainingOrNumeroContainingOrderByNome(str, str);
		return VacaDto.converter(vacas.stream().map(v -> {
			v.setCor(setCor(v));
			return v;
		}).collect(Collectors.toList()));
	}

	@GetMapping("/calcular/{numero}/{data}")
	@Transactional
	private ResponseEntity<Vaca> calcularDatas(@PathVariable String numero, @PathVariable String data) {

		Vaca vaca = vacasRepository.findById(numero).orElseThrow(() -> new NumeroEcxeption("Id não encontrado"));
		try {
			if (vaca.getParto() != (null)) {
				if (vaca.getParto().isBefore(LocalDate.parse(data, formater))) {
					Integer getnCrias = vaca.getnCrias();
					vaca.setnCrias(getnCrias + 1);
				}
			}
		} catch (DateTimeParseException e) {
			throw new DataEcxeption("Formato da data Inválido");
		}
		vaca.setEnsiminacao(LocalDate.parse(data, formater));
		vaca.setSecagem(vaca.getEnsiminacao().plusDays(253L));
		vaca.setParto(vaca.getSecagem().plusDays(30L));
		vaca.setNovaEnsiminacao(vaca.getParto().plusDays(40L));

		vacasRepository.save(vaca);
		return ResponseEntity.ok(vaca);
	}

	@GetMapping("/cadastrar/{numero}/{nome}")
	private ResponseEntity<Vaca> cadastrar(@PathVariable @Valid @NotNull @NotEmpty String numero,
			@PathVariable @Valid @NotNull @NotEmpty String nome,
			@RequestParam(defaultValue = "0", required = false) String n) {
		Vaca vaca = new Vaca(numero, nome, Integer.valueOf(n));
		vacasRepository.save(vaca);

		return ResponseEntity.ok(vaca);
	}

	@GetMapping("/alterar/{numero}/{nome}")
	@Transactional
	private ResponseEntity<Vaca> alterar(@PathVariable @Valid @NotNull @NotEmpty String numero,
			@PathVariable @Valid @NotNull @NotEmpty String nome,
			@RequestParam(defaultValue = "0", required = false) String n) {
		Vaca vaca = vacasRepository.findById(numero).orElseThrow(() -> new VacaEcxeption("Numero nao existe"));
		vaca.setNumero(numero);
		vaca.setNome(nome);
		if (Integer.valueOf(n) > Integer.valueOf("0"))
			vaca.setnCrias(Integer.valueOf(n));
		vacasRepository.save(vaca);
		return ResponseEntity.ok(vaca);
	}

	@GetMapping("/deletar/{n}")
	private ResponseEntity<Vaca> deletar(@PathVariable String n) {
		vacasRepository.deleteById(n);
		return ResponseEntity.ok().build();
	}

	private boolean corExiste(Optional<String> cor) {
		return cores.stream().filter(z -> z.equals(cor.orElse("0"))).count() < 1L;
	}

	private static String setCor(Vaca v) {
		if (v.getEnsiminacao() == null || v.getNovaEnsiminacao() == null || v.getParto() == null
				|| v.getSecagem() == null) {
			return "branco";
		}
		LocalDate now = LocalDate.now();
		if (now.isBefore(v.getSecagem())) {
			return "branco";
		} else if (now.isBefore(v.getParto())) {
			if (now.isAfter(v.getSecagem().plusDays(20))) {
				return "cinza";
			}
			return "amarelo";
		} else if (now.isBefore(v.getNovaEnsiminacao())) {
			return "branco";
		} else if (now.isAfter(v.getNovaEnsiminacao().plusDays(40L))) {
			return "vermelho";
		}
		return "verde";
	}
}
