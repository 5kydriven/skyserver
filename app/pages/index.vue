<script setup lang="ts">
useSeoMeta({
  title: 'SKYSERVER Homelab',
  description: 'SKYSERVER homelab services',
})

const services = [
  {
    title: 'Nextcloud',
    description: 'Files and collaboration',
    to: 'https://nextcloud.skydriven.xyz',
  },
  {
    title: 'Uptime Kuma',
    description: 'Service status · protected',
    to: 'https://uptime.skydriven.xyz',
  },
  {
    title: 'Beszel',
    description: 'Host metrics · protected',
    to: 'https://beszel.skydriven.xyz',
  },
  {
    title: 'Coolify',
    description: 'Deployment control · protected',
    to: 'https://coolify.skydriven.xyz',
  },
]
</script>

<template>
  <main class="flex min-h-dvh items-center justify-center px-6 py-8 sm:px-8">
    <UCard
      class="w-full max-w-[760px] rounded-2xl bg-elevated/90 shadow-2xl"
      :ui="{ body: 'p-6 sm:p-10' }"
    >
      <header>
        <p class="text-xs font-bold tracking-[0.14em] text-primary uppercase">
          SKYSERVER · HOMELAB
        </p>
        <h1
          class="mt-2 text-3xl font-bold tracking-tight text-highlighted sm:text-5xl"
        >
          Welcome to the homelab.
        </h1>
        <p class="mt-3 text-muted">
          Choose a service below. Administrative services require the configured
          access policy.
        </p>
      </header>

      <section
        class="mt-8 grid gap-4 sm:grid-cols-2"
        aria-label="Homelab services"
      >
        <UPageCard
          v-for="service in services"
          :key="service.to"
          v-bind="service"
          :as="{ title: 'h2' }"
          class="bg-default/60 transition-transform motion-safe:hover:-translate-y-0.5 focus-within:ring-2 focus-within:ring-primary"
          :ui="{
            container: 'p-4 sm:p-4',
            title: 'text-base font-semibold',
            description: 'text-sm',
          }"
        />
      </section>

      <footer class="mt-8 text-xs text-muted">
        Public application routes are served through the Cloudflare Tunnel.
      </footer>
    </UCard>
  </main>
</template>
