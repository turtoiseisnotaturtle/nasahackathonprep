import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

export function createScene(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(devicePixelRatio);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#0b0f17');

  const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
  camera.position.set(0, 1.2, 4);
  const controls = new OrbitControls(camera, canvas);
  controls.target.set(0, 1, 0);
  controls.update();

  scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 2));
  const sun = new THREE.DirectionalLight(0xffffff, 2);
  sun.position.set(3, 5, 4);
  scene.add(sun);

  const pivot = new THREE.Group();          // everything we rotate
  scene.add(pivot);
  new GLTFLoader().load('/models/Xbot.glb',
    gltf => pivot.add(gltf.scene),
    undefined,
    () => pivot.add(fallbackFigure()));     // if the model is missing

  let targetY = 0;
  function resize() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  }
  addEventListener('resize', resize);
  resize();

  renderer.setAnimationLoop(() => {
    pivot.rotation.y += (targetY - pivot.rotation.y) * 0.15;   // smooth easing
    renderer.render(scene, camera);
  });

  return { rotateBy(delta) { targetY += delta; } };
}

function fallbackFigure() {
  const m = new THREE.MeshStandardMaterial({ color: 0xcccccc });
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.25, 0.8, 8, 16), m);
  body.position.y = 1;
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.18, 24, 24), m);
  head.position.y = 1.75;
  const visor = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.08, 0.05),
    new THREE.MeshStandardMaterial({ color: 0x3b82f6 }));
  visor.position.set(0, 1.78, 0.17);
  g.add(body, head, visor);
  return g;
}

