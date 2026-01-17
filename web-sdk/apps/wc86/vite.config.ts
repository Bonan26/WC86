import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	resolve: {
		alias: {
			$game: '/src/game',
			$components: '/src/components',
		},
	},
	server: {
		port: 5173,
		strictPort: false,
	},
});
