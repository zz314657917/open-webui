<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, getContext } from 'svelte';
	import type { Writable } from 'svelte/store';
	import type { i18n as i18nType } from 'i18next';
	import { goto } from '$app/navigation';

	import { user } from '$lib/stores';
	import { imageGenerations, imageEdits } from '$lib/apis/images';

	import Spinner from '$lib/components/common/Spinner.svelte';
	import Image from '$lib/components/common/Image.svelte';
	import ImageGenerationGroup from '$lib/components/chat/Messages/ResponseMessage/ImageGenerationGroup.svelte';

	const i18n = getContext<Writable<i18nType>>('i18n');

	let loaded = false;
	let loading = false;

	let prompt = '';
	let sourceImages: string[] = [];
	let generatedImageGroups: {
		id: string;
		prompt: string;
		images: { type: string; url: string }[];
	}[] = [];

	let promptTextareaElement: HTMLTextAreaElement;
	let fileInputElement: HTMLInputElement;

	const resizePromptTextarea = () => {
		if (promptTextareaElement) {
			promptTextareaElement.style.height = '';
			promptTextareaElement.style.height = Math.min(promptTextareaElement.scrollHeight, 150) + 'px';
		}
	};

	const handleFileUpload = (event: Event) => {
		const input = event.target as HTMLInputElement;
		if (input.files) {
			Array.from(input.files).forEach((file) => {
				const reader = new FileReader();
				reader.onload = (e) => {
					if (e.target?.result) {
						sourceImages = [...sourceImages, e.target.result as string];
					}
				};
				reader.readAsDataURL(file);
			});
		}
	};

	const handleDrop = (event: DragEvent) => {
		event.preventDefault();
		const files = event.dataTransfer?.files;
		if (files) {
			Array.from(files).forEach((file) => {
				if (file.type.startsWith('image/')) {
					const reader = new FileReader();
					reader.onload = (e) => {
						if (e.target?.result) {
							sourceImages = [...sourceImages, e.target.result as string];
						}
					};
					reader.readAsDataURL(file);
				}
			});
		}
	};

	const removeImage = (index: number) => {
		sourceImages = sourceImages.filter((_, i) => i !== index);
	};

	const submitHandler = async () => {
		if (!prompt.trim()) {
			toast.error($i18n.t('Please enter a prompt'));
			return;
		}

		loading = true;
		try {
			let result;
			if (sourceImages.length > 0) {
				console.log('Calling imageEdits with', sourceImages.length, 'images');
				result = await imageEdits(
					localStorage.token,
					sourceImages.length === 1 ? sourceImages[0] : sourceImages,
					prompt
				);
			} else {
				console.log('Calling imageGenerations');
				result = await imageGenerations(localStorage.token, prompt);
			}

			console.log('Result:', result);
			if (result) {
				const images = result.map((image: { url: string }) => ({ ...image, type: 'image' }));
				generatedImageGroups = [
					{ id: crypto.randomUUID(), prompt, images },
					...generatedImageGroups
				];
			}
		} catch (error) {
			console.error('Image generation/edit error:', error);
			toast.error(`${error}`);
		} finally {
			loading = false;
		}
	};

	onMount(async () => {
		if ($user?.role !== 'admin') {
			await goto('/');
			return;
		}
		loaded = true;
	});
</script>

<div class=" flex flex-col justify-between w-full overflow-y-auto h-full">
	<div class="mx-auto w-full md:px-0 h-full">
		<div class=" flex flex-col h-full px-4">
			<!-- Results Area -->
			<div
				class=" pt-0.5 pb-2.5 flex flex-col justify-between w-full flex-auto overflow-auto h-0"
				id="images-container"
			>
				<div class=" h-full w-full flex flex-col">
					<div class="flex-1 p-1">
						{#if generatedImageGroups.length > 0}
							<div class="space-y-3">
								{#each generatedImageGroups as group (group.id)}
									{#if group.images.length > 1}
										<ImageGenerationGroup
											images={group.images}
											alt={group.prompt}
											className="w-full"
										/>
									{:else if group.images.length === 1}
										{@const image = group.images[0]}
										<Image
											src={image.url}
											alt={group.prompt}
											imageClassName="w-full max-w-sm aspect-square object-cover rounded-lg border border-gray-100/30 dark:border-gray-850/30"
										/>
									{/if}
								{/each}
							</div>
						{:else}
							<div
								class="h-full flex items-center justify-center text-gray-400 dark:text-gray-600 text-sm"
							>
								{$i18n.t('Generated images will appear here')}
							</div>
						{/if}
					</div>
				</div>
			</div>

			<!-- Input Area -->
			<div class="pb-3">
				<div
					class="border border-gray-100/30 dark:border-gray-850/30 w-full px-3 py-2.5 rounded-xl"
				>
					<!-- Source Images -->
					{#if sourceImages.length > 0}
						<div class="flex flex-wrap gap-2 mb-2">
							{#each sourceImages as image, index}
								<div class=" relative group">
									<div class="relative flex items-center">
										<img src={image} alt="" class="size-10 rounded-xl object-cover" />
									</div>
									<div class=" absolute -top-1 -right-1">
										<button
											class=" bg-white text-black border border-white rounded-full group-hover:visible invisible transition"
											type="button"
											aria-label={$i18n.t('Remove image')}
											on:click={() => removeImage(index)}
										>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												viewBox="0 0 20 20"
												fill="currentColor"
												aria-hidden="true"
												class="size-4"
											>
												<path
													d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
												/>
											</svg>
										</button>
									</div>
								</div>
							{/each}
						</div>
					{/if}

					<!-- Prompt Textarea -->
					<div class="py-0.5">
						<textarea
							bind:this={promptTextareaElement}
							bind:value={prompt}
							class=" w-full h-full bg-transparent resize-none outline-hidden text-sm"
							placeholder={sourceImages.length > 0
								? $i18n.t('Describe the edit...')
								: $i18n.t('Describe the image...')}
							on:input={resizePromptTextarea}
							on:focus={resizePromptTextarea}
							on:keydown={(e) => {
								if (e.key === 'Enter' && (e.metaKey || e.ctrlKey) && !loading) {
									e.preventDefault();
									submitHandler();
								}
							}}
							rows="2"
						></textarea>
					</div>

					<!-- Actions -->
					<div class="flex justify-between items-center gap-2 mt-2">
						<div class="shrink-0">
							<input
								type="file"
								accept="image/*"
								multiple
								class="hidden"
								bind:this={fileInputElement}
								on:change={handleFileUpload}
							/>
							<button
								type="button"
								class="px-3.5 py-1.5 text-sm font-medium bg-gray-50 hover:bg-gray-100 text-gray-900 dark:bg-gray-850 dark:hover:bg-gray-800 dark:text-gray-200 transition rounded-lg"
								on:click={() => fileInputElement?.click()}
								on:dragover|preventDefault
								on:drop={handleDrop}
							>
								{$i18n.t('Add Image')}
							</button>
						</div>

						<div class="flex gap-2 shrink-0">
							{#if !loading}
								<button
									disabled={prompt.trim() === ''}
									class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-lg disabled:opacity-50 disabled:cursor-not-allowed"
									on:click={submitHandler}
								>
									{$i18n.t('Run')}
								</button>
							{:else}
								<button
									class="px-3.5 py-1.5 text-sm font-medium bg-gray-300 text-black transition rounded-lg flex items-center gap-2"
									disabled
								>
									<Spinner className="size-4" />
									{$i18n.t('Running...')}
								</button>
							{/if}
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
