(function waitForElements(ids, cb, timeout = 10000, interval = 100) {
  const start = Date.now();
  const iv = setInterval(() => {
    const found = ids.map(id => document.querySelector(id));
    if (found.every(el => el !== null)) {
      clearInterval(iv);
      cb(...found);
      return;
    }
    if (Date.now() - start > timeout) {
      clearInterval(iv);
      console.warn('waitForElements: timeout waiting for', ids);
    }
  }, interval);
})(
  ['#input-column', '#extracted-prompt'], // selectors to wait for
  (inputCol, outputWrapper) => {
    // `outputWrapper` is the container that wraps the textbox; find the textarea inside it
    const textarea = outputWrapper.querySelector('textarea') || document.querySelector('#extracted-prompt textarea');

    if (!textarea) {
      console.warn('extracted-prompt textarea not found inside wrapper, trying global query');
    }

    // helper to compute rows based on viewport or target height
    function rowsForViewport(width, height) {
        if(width < 400){
            return 3;
        }
        else if(height < 600){
            return Math.floor(height/20);
        }
        else if(height < 800){
          return Math.floor(height/25);
        }
        else{
            return Math.floor(height/30);
        }
    }

    function syncHeightAndRows() {
      // attempt to get the current elements (in case of DOM reattach)
      const src = document.querySelector('#input-column');
      const outWrapper = document.querySelector('#extracted-prompt');
      const ta = outWrapper ? outWrapper.querySelector('textarea') : textarea;
      if (!src || !outWrapper || !ta) return;

      // match wrapper height
      const targetHeight = src.offsetHeight;
      if(window.innerWidth>500){
      outWrapper.style.height = targetHeight + 'px';
      }
      else{
        outWrapper.style.height = 100 + 'px';
      }
      // set textarea rows to fit target height (uses computed line-height)
      const rows = rowsForViewport(window.innerWidth, window.innerHeight, targetHeight);
      ta.rows = rows;
      // also explicitly set textarea height (small buffer to avoid scroll)
      const lineHeight = parseFloat(getComputedStyle(ta).lineHeight) || 20;
      ta.style.height = (rows * lineHeight + 8) + 'px';
    }

    // initial sync
    syncHeightAndRows();

    // Observe input column for size changes and update target
    try {
      const ro = new ResizeObserver(syncHeightAndRows);
      ro.observe(inputCol);
    } catch (e) {
      // fallback: listen to window resize
      window.addEventListener('resize', syncHeightAndRows);
    }

    // Also observe mutations inside the input column (in case content changes)
    try {
      const mo = new MutationObserver(syncHeightAndRows);
      mo.observe(inputCol, { childList: true, subtree: true, characterData: true });
    } catch (e) {
      // ignore if MutationObserver not available
    }
  }
);
