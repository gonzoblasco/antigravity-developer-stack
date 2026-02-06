# Accessibility Checklist

## ARIA & Semantics

- [ ] Usar elementos semánticos (`<nav>`, `<main>`, `<article>`, `<section>`)
- [ ] Roles ARIA solo cuando no hay elemento semántico equivalente
- [ ] `aria-label` o `aria-labelledby` en regiones y widgets
- [ ] `aria-describedby` para instrucciones adicionales
- [ ] `aria-live` para contenido dinámico

## Navegación por Teclado

- [ ] Todo interactivo accesible con Tab
- [ ] Orden de tabulación lógico (`tabindex` correctos)
- [ ] Atajos de teclado documentados (si existen)
- [ ] Sin trampas de foco (keyboard traps)
- [ ] Skip links para navegación principal

## Focus Management

- [ ] `:focus-visible` con outline visible
- [ ] Focus moved correctly on modals/dialogs
- [ ] Focus returned after closing overlays
- [ ] No `outline: none` sin alternativa visible

## Forms

- [ ] Todos los inputs tienen `<label>` asociado
- [ ] Campos requeridos marcados con `aria-required`
- [ ] Errores asociados con `aria-describedby`
- [ ] Mensajes de error claros y específicos
- [ ] Grupos de radio/checkbox con `<fieldset>` y `<legend>`

## Images & Media

- [ ] `alt` descriptivo en imágenes informativas
- [ ] `alt=""` en imágenes decorativas
- [ ] Captions/transcripts para video/audio

## Color & Contrast

- [ ] Contraste mínimo 4.5:1 para texto normal
- [ ] Contraste mínimo 3:1 para texto grande
- [ ] Información no transmitida solo por color
- [ ] Dark mode con contrastes correctos

## Testing

```bash
# Herramientas recomendadas
- axe DevTools (Chrome extension)
- WAVE Evaluation Tool
- Lighthouse Accessibility audit
- VoiceOver (macOS) / NVDA (Windows)
```

## Quick Wins

1. Usar `<button>` para acciones, `<a>` para navegación
2. `type="button"` en buttons que no son submit
3. `lang` attribute en `<html>`
4. Page `<title>` descriptivo y único
