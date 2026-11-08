export function connectGestures(url, dispatch, onStatus) {
  (function open() {
    const ws = new WebSocket(url);
    ws.onopen = () => onStatus('connected');
    ws.onmessage = e => dispatch(JSON.parse(e.data));
    ws.onclose = () => { onStatus('disconnected'); setTimeout(open, 2000); }; // auto-reconnect
  })();
}