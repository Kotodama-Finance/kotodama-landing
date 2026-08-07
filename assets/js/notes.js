/* =========================================================================
   El buscador del archivo de notas (/notes/).

   Filtra EL LISTADO QUE YA ESTÁ EN EL HTML — lo genera make-notes.py y los
   crawlers lo leen sin ejecutar nada—: este script no renderiza contenido,
   sólo esconde filas. La búsqueda por CONTENIDO usa el índice
   /notes/search-index.json (título + lead + texto completo de cada nota),
   emparejado con las filas por data-url.

   Progresivo a propósito: el campo de búsqueda nace con `hidden` en el HTML
   y se destapa acá, sólo cuando el índice cargó Y hay algo que buscar. Sin
   JS (o si el fetch falla) la página es el listado completo, que es
   exactamente lo que era antes de que existiera este archivo.

   Sin módulos ni dependencias: es la segunda página con JS del sitio
   (decisión del autor — «cero JS» es propiedad de las páginas de lectura,
   no de una herramienta) y no necesita más que esto.
   ========================================================================= */
(function () {
  var caja = document.querySelector('.notes-search');
  var input = document.getElementById('notes-search');
  var lista = document.querySelector('.notes-list');
  if (!caja || !input || !lista) return;

  fetch('/notes/search-index.json')
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(function (datos) {
      var filas = [];
      (datos.notes || []).forEach(function (n) {
        // El selector escapa comillas por las dudas; hoy las rutas son
        // /hajime/<slug>/ y no traen ninguna.
        var li = lista.querySelector('[data-url="' + n.url.replace(/"/g, '\\"') + '"]');
        if (li) {
          filas.push({
            li: li,
            texto: (n.title + ' ' + n.lead + ' ' + n.text).toLowerCase(),
          });
        }
      });
      if (!filas.length) return; // nada que buscar: el campo no aparece

      caja.hidden = false;
      input.addEventListener('input', function () {
        // Términos separados por espacio, TODOS tienen que aparecer
        // (en título, lead o cuerpo). Substring simple: para veinte notas
        // no hace falta más, y un ranking sería fingir precisión.
        var terminos = input.value.toLowerCase().split(/\s+/).filter(Boolean);
        filas.forEach(function (f) {
          f.li.hidden = !terminos.every(function (t) {
            return f.texto.indexOf(t) !== -1;
          });
        });
      });
    })
    .catch(function (err) {
      // EN INGLÉS aunque los comentarios vayan en castellano: un console.warn
      // se ejecuta — es interfaz, la misma regla que main.js.
      console.warn('[notes] search index unavailable; the full list stands.', err);
    });
})();
