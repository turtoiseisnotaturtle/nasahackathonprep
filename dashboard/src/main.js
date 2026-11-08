import './style.css';
import { createScene } from './scene.js';
import { createUI } from './ui.js';
import { on, dispatch } from './commandBus.js';
import { connectGestures } from './gestureClient.js';

const viewer = createScene(document.getElementById('viewer'));
const ui = createUI();

on('rotate',  c => viewer.rotateBy(c.delta));
on('select',  c => (c.dir === 'next' ? ui.next() : ui.prev()));
on('slider',  c => ui.nudge(c.delta));
on('gesture', c => (document.getElementById('gesture-name').textContent = c.name));

// Keyboard fallback, so you can test without the camera
addEventListener('keydown', e => {
  const map = {
    ArrowLeft:  { type: 'rotate', delta: -0.3 }, ArrowRight: { type: 'rotate', delta: 0.3 },
    ArrowUp:    { type: 'slider', delta: 0.05 }, ArrowDown:  { type: 'slider', delta: -0.05 },
    Tab:        { type: 'select', dir: e.shiftKey ? 'prev' : 'next' },
  };
  if (map[e.key]) { e.preventDefault(); dispatch(map[e.key]); }
});

connectGestures('ws://localhost:8765', dispatch,
  s => (document.getElementById('status').textContent = `Gesture: ${s}`));