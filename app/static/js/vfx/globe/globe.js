import AssetURLs from "../../_globals/AssetUrls.js";

const MapImageURL = AssetURLs.MapImageURL;

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('globe-container');
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(container.offsetWidth, container.offsetHeight);
  container.appendChild(renderer.domElement);

  // Create dots geometry
  const DOT_COUNT = 10000;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(DOT_COUNT * 3);
  const colors = new Float32Array(DOT_COUNT * 3);

  const mapImage = new Image();
  mapImage.src = MapImageURL;

  mapImage.onload = () => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = mapImage.width;
    canvas.height = mapImage.height;
    context.drawImage(mapImage, 0, 0, mapImage.width, mapImage.height);
    const imageData = context.getImageData(0, 0, mapImage.width, mapImage.height).data;

    for (let i = 0; i < DOT_COUNT; i++) {
      const phi = Math.acos(2 * Math.random() - 1);
      const theta = 2 * Math.PI * Math.random();

      const x = 5 * Math.sin(phi) * Math.cos(theta);
      const y = 5 * Math.sin(phi) * Math.sin(theta);
      const z = 5 * Math.cos(phi);

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;

      const uv = pointToUV(x, y, z);
      const color = sampleImage(uv, imageData, mapImage.width, mapImage.height);

      colors[i * 3] = color.r / 255;
      colors[i * 3 + 1] = color.g / 255;
      colors[i * 3 + 2] = color.b / 255;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({ size: 0.2, vertexColors: true });  // Increase dot size
    const dots = new THREE.Points(geometry, material);
    scene.add(dots);

    camera.position.z = 10;  // Bring the camera closer for a larger globe

    // Animation loop
    function animate() {
      requestAnimationFrame(animate);
      dots.rotation.y += 0.001;
      renderer.render(scene, camera);
    }
    animate();

    // Handle window resize
    window.addEventListener('resize', () => {
      camera.aspect = container.offsetWidth / container.offsetHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.offsetWidth, container.offsetHeight);
    });
  };

  function pointToUV(x, y, z) {
    const u = 0.5 + Math.atan2(z, x) / (2 * Math.PI);
    const v = 0.5 - Math.asin(y / 5) / Math.PI;
    return { u, v };
  }

  function sampleImage(uv, imageData, width, height) {
    const x = Math.floor(uv.u * width);
    const y = Math.floor(uv.v * height);
    const index = (y * width + x) * 4;
    return {
      r: imageData[index],
      g: imageData[index + 1],
      b: imageData[index + 2],
    };
  }
});
