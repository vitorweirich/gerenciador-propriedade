package com.teste.vacas.vacas.validacaoconfig;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.MessageSource;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.http.HttpStatus;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;


@RestControllerAdvice
public class ErroDeValidacaoConfig {

	@Autowired
	private MessageSource messageSource;

	@ResponseStatus(code = HttpStatus.BAD_REQUEST)
	@ExceptionHandler(MethodArgumentNotValidException.class)
	public List<ErroDeFormularioDto> handle(MethodArgumentNotValidException exception) {
		List<ErroDeFormularioDto> dto = new ArrayList<ErroDeFormularioDto>();
		List<FieldError> fieldErrors = exception.getBindingResult().getFieldErrors();

		fieldErrors.forEach(e -> {
			String msg = messageSource.getMessage(e, LocaleContextHolder.getLocale());
			if(msg.contains("^\\d^\\d{2}/\\d{2}/\\d{4}$/\\d^\\d{2}/\\d{2}/\\d{4}$/\\d{4}$")) {
				msg = msg.substring(0, msg.length() - 53) + "'dd/MM/aaaa'";
			}
			ErroDeFormularioDto erro = new ErroDeFormularioDto(e.getField(), msg);
			dto.add(erro);
		});

		return dto;
	}
	
	@ResponseStatus(code = HttpStatus.BAD_REQUEST)
	@ExceptionHandler(VacaEcxeption.class)
	public ErroDeFormularioDto handle(VacaEcxeption exception) {

		return new ErroDeFormularioDto("numero", exception.getMessage());
	}
	
	@ResponseStatus(code = HttpStatus.BAD_REQUEST)
	@ExceptionHandler(NumeroEcxeption.class)
	public ErroDeFormularioDto handle(NumeroEcxeption exception) {

		return new ErroDeFormularioDto("numero", exception.getMessage());
	}
	
	@ResponseStatus(code = HttpStatus.BAD_REQUEST)
	@ExceptionHandler(DataEcxeption.class)
	public ErroDeFormularioDto handle(DataEcxeption exception) {

		return new ErroDeFormularioDto("data", exception.getMessage());
	}
}
