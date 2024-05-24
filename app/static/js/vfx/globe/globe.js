// Set up the scene
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth / 2, window.innerHeight / 2);
const container = document.getElementById('globe-container');
container.appendChild(renderer.domElement);

// Create the globe
const geometry = new THREE.SphereGeometry(5, 32, 32);
const texture = new THREE.TextureLoader().load('earth_texture.jpg');
const material = new THREE.MeshBasicMaterial({ map: texture });
const globe = new THREE.Mesh(geometry, material);
scene.add(globe);

// Set up camera
camera.position.z = 10;

// Add animation
function animate() {
  requestAnimationFrame(animate);
  globe.rotation.y += 0.001;
  renderer.render(scene, camera);
}
animate();