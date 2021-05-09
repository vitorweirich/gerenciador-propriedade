package com.teste.vacas.vacas.modelo.dto;

import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Locale;
import java.util.stream.Collectors;

import com.teste.vacas.vacas.modelo.Vaca;

public class VacaDto {

	private static DateTimeFormatter formaterBr = DateTimeFormatter.ofPattern("dd-MM-yyyy")
			.withLocale(new Locale("pt", "BR"));

	private String numero;
	private String nome;
	private String ensiminacao;
	private String secagem;
	private String parto;
	private String novaEnsiminacao;
	private Integer nCrias;
	private String cor;

	public VacaDto(Vaca vaca) {
		this.numero = vaca.getNumero();
		this.nome = vaca.getNome();
		if (vaca.getEnsiminacao() == null || vaca.getSecagem() == null || vaca.getParto() == null || vaca.getNovaEnsiminacao() == null) {
			this.ensiminacao = "";
			this.secagem = "";
			this.parto = "";
			this.novaEnsiminacao = "";	
		} else {
			this.ensiminacao = vaca.getEnsiminacao().format(formaterBr).replace('-', '/');
			this.secagem = vaca.getSecagem().format(formaterBr).replace('-', '/');
			this.parto = vaca.getParto().format(formaterBr).replace('-', '/');
			this.novaEnsiminacao = vaca.getNovaEnsiminacao().format(formaterBr).replace('-', '/');			
		}
		this.nCrias = vaca.getnCrias();
		this.cor = vaca.getCor();
	}

	public static DateTimeFormatter getFormaterBr() {
		return formaterBr;
	}

	public static void setFormaterBr(DateTimeFormatter formaterBr) {
		VacaDto.formaterBr = formaterBr;
	}

	public String getNumero() {
		return numero;
	}

	public void setNumero(String numero) {
		this.numero = numero;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public String getEnsiminacao() {
		return ensiminacao;
	}

	public void setEnsiminacao(String ensiminacao) {
		this.ensiminacao = ensiminacao;
	}

	public String getSecagem() {
		return secagem;
	}

	public void setSecagem(String secagem) {
		this.secagem = secagem;
	}

	public String getParto() {
		return parto;
	}

	public void setParto(String parto) {
		this.parto = parto;
	}

	public String getNovaEnsiminacao() {
		return novaEnsiminacao;
	}

	public void setNovaEnsiminacao(String novaEnsiminacao) {
		this.novaEnsiminacao = novaEnsiminacao;
	}

	public Integer getnCrias() {
		return nCrias;
	}

	public void setnCrias(Integer nCrias) {
		this.nCrias = nCrias;
	}

	public String getCor() {
		return cor;
	}

	public void setCor(String cor) {
		this.cor = cor;
	}

	public static List<VacaDto> converter(List<Vaca> list) {
		return list.stream().map(VacaDto::new).collect(Collectors.toList());
	}

}
