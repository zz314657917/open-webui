<script lang="ts">
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import type { i18n as i18nType } from 'i18next';
	import { toast } from 'svelte-sonner';

	import { WEBUI_BASE_URL } from '$lib/constants';
	import { safeImageUrl } from '$lib/utils/safeImageUrl';
	import ImagePreview from '$lib/components/common/ImagePreview.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import Download from '$lib/components/icons/Download.svelte';
	import ChevronLeft from '$lib/components/icons/ChevronLeft.svelte';
	import ChevronRight from '$lib/components/icons/ChevronRight.svelte';
	import ArrowsPointingOut from '$lib/components/icons/ArrowsPointingOut.svelte';
	import Grid from '$lib/components/icons/Grid.svelte';

	type ImageFile = {
		type: string;
		url: string;
		name?: string;
		content_type?: string;
	};

	export let images: ImageFile[] = [];
	export let alt = '';
	export let className = 'my-2 w-full max-w-3xl';

	const i18n = getContext<Writable<i18nType>>('i18n');

	let selectedIndex = 0;
	let showImagePreview = false;

	const getSafeImageUrl = (src: string) => {
		return safeImageUrl(src.startsWith('/') ? `${WEBUI_BASE_URL}${src}` : src);
	};

	const t = (key: string, fallback: string) => {
		const value = $i18n.t(key);
		return value || fallback;
	};

	$: if (images.length > 0 && selectedIndex > images.length - 1) {
		selectedIndex = images.length - 1;
	}

	$: selectedImage = images[selectedIndex];
	$: selectedSrc = getSafeImageUrl(selectedImage?.url ?? '');

	const selectPrevious = () => {
		if (images.length === 0) {
			return;
		}

		selectedIndex = selectedIndex === 0 ? images.length - 1 : selectedIndex - 1;
	};

	const selectNext = () => {
		if (images.length === 0) {
			return;
		}

		selectedIndex = selectedIndex === images.length - 1 ? 0 : selectedIndex + 1;
	};

	const saveBlob = (blob: Blob, fileName: string) => {
		const blobUrl = URL.createObjectURL(blob);
		const anchor = document.createElement('a');
		anchor.href = blobUrl;
		anchor.download = fileName;
		anchor.click();
		URL.revokeObjectURL(blobUrl);
	};

	const downloadSelected = async () => {
		try {
			const response = await fetch(selectedSrc);
			const blob = await response.blob();
			const mimeType = blob.type || selectedImage?.content_type || 'image/png';
			const extension = mimeType.split('/')[1] || 'png';
			const fileName =
				selectedImage?.name ||
				`${t('Generated Image', 'Generated Image').toLowerCase().replace(/ /g, '_')}-${selectedIndex + 1}.${extension}`;

			saveBlob(new Blob([blob], { type: mimeType }), fileName);
		} catch (error) {
			console.error('Failed to download image:', error);
			toast.error($i18n.t('Failed to download image'));
		}
	};

	const downloadAll = async () => {
		try {
			const JSZip = (await import('jszip')).default;
			const zip = new JSZip();

			await Promise.all(
				images.map(async (image, index) => {
					const src = getSafeImageUrl(image.url);
					const response = await fetch(src);
					const blob = await response.blob();
					const mimeType = blob.type || image.content_type || 'image/png';
					const extension = mimeType.split('/')[1] || 'png';
					const fileName =
						image.name ||
						`${t('Generated Image', 'Generated Image').toLowerCase().replace(/ /g, '_')}-${index + 1}.${extension}`;

					zip.file(fileName, blob);
				})
			);

			const zipBlob = await zip.generateAsync({ type: 'blob' });
			saveBlob(zipBlob, `generated-images-${Date.now()}.zip`);
		} catch (error) {
			console.error('Failed to download images:', error);
			toast.error($i18n.t('Failed to download image'));
		}
	};

	const downloadAllLabel = () => {
		const all = t('All', 'All');
		const download = t('Download', 'Download');

		if ($i18n.language?.startsWith('zh')) {
			return `${download}${all}`;
		}

		return `${download} ${all}`.trim();
	};
</script>

{#if images.length > 0}
	<ImagePreview bind:show={showImagePreview} src={selectedSrc} {alt} />

	<div
		class="{className} overflow-hidden rounded-lg border border-gray-100/80 bg-white/70 shadow-xs dark:border-gray-850 dark:bg-gray-950/40"
	>
		<div
			class="flex items-center justify-between gap-2 border-b border-gray-100/80 px-3 py-2 dark:border-gray-850"
		>
			<div class="flex min-w-0 items-center gap-2">
				<div
					class="flex size-7 shrink-0 items-center justify-center rounded-md bg-gray-50 text-gray-700 dark:bg-gray-900 dark:text-gray-200"
					aria-hidden="true"
				>
					<Grid className="size-4" strokeWidth="1.7" />
				</div>
				<div class="min-w-0">
					<div class="truncate text-sm font-medium text-gray-900 dark:text-gray-100">
						{t('Images', 'Images')}
					</div>
					<div class="text-xs text-gray-500 dark:text-gray-400">
						{selectedIndex + 1} / {images.length}
					</div>
				</div>
			</div>

			<div class="flex shrink-0 items-center gap-1">
				<Tooltip content={t('Previous message', 'Previous')}>
					<button
						class="rounded-md p-1.5 text-gray-600 transition hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-850 dark:hover:text-white"
						type="button"
						aria-label={t('Previous message', 'Previous')}
						on:click={selectPrevious}
					>
						<ChevronLeft className="size-4" strokeWidth="2" />
					</button>
				</Tooltip>

				<Tooltip content={t('Next message', 'Next')}>
					<button
						class="rounded-md p-1.5 text-gray-600 transition hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-850 dark:hover:text-white"
						type="button"
						aria-label={t('Next message', 'Next')}
						on:click={selectNext}
					>
						<ChevronRight className="size-4" strokeWidth="2" />
					</button>
				</Tooltip>

				<Tooltip content={t('Show image preview', 'Show image preview')}>
					<button
						class="rounded-md p-1.5 text-gray-600 transition hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-850 dark:hover:text-white"
						type="button"
						aria-label={t('Show image preview', 'Show image preview')}
						on:click={() => {
							showImagePreview = true;
						}}
					>
						<ArrowsPointingOut className="size-4" strokeWidth="1.8" />
					</button>
				</Tooltip>

				<Tooltip content={t('Download', 'Download')}>
					<button
						class="rounded-md p-1.5 text-gray-600 transition hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-850 dark:hover:text-white"
						type="button"
						aria-label={t('Download', 'Download')}
						on:click={downloadSelected}
					>
						<Download className="size-4" strokeWidth="1.8" />
					</button>
				</Tooltip>

				<Tooltip content={downloadAllLabel()}>
					<button
						class="flex items-center gap-1 rounded-md px-2 py-1.5 text-xs font-medium text-gray-600 transition hover:bg-gray-100 hover:text-gray-900 dark:text-gray-300 dark:hover:bg-gray-850 dark:hover:text-white"
						type="button"
						aria-label={downloadAllLabel()}
						on:click={downloadAll}
					>
						<Download className="size-3.5" strokeWidth="1.8" />
						<span class="hidden sm:inline">{t('All', 'All')}</span>
					</button>
				</Tooltip>
			</div>
		</div>

		<button
			class="block w-full bg-gray-50 text-left dark:bg-gray-900/40"
			type="button"
			aria-label={t('Show image preview', 'Show image preview')}
			on:click={() => {
				showImagePreview = true;
			}}
		>
			<img
				src={selectedSrc}
				{alt}
				class="h-auto max-h-[34rem] w-full object-contain"
				draggable="false"
				data-cy="image-generation-group-selected"
			/>
		</button>

		<div class="grid grid-cols-4 gap-1.5 p-2 sm:grid-cols-6 md:grid-cols-8">
			{#each images as image, index}
				<button
					class="relative aspect-square overflow-hidden rounded-md border transition {index ===
					selectedIndex
						? 'border-gray-900 ring-2 ring-gray-900/10 dark:border-white dark:ring-white/15'
						: 'border-gray-100 opacity-80 hover:opacity-100 dark:border-gray-850'}"
					type="button"
					aria-label={`${t('Generated Image', 'Generated Image')} ${index + 1}`}
					on:click={() => {
						selectedIndex = index;
					}}
				>
					<img
						src={getSafeImageUrl(image.url)}
						alt=""
						class="h-full w-full object-cover"
						draggable="false"
					/>
				</button>
			{/each}
		</div>
	</div>
{/if}
