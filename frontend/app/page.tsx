import { ImageAnnotator } from "@/components/image-annotator"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-4 md:p-8">
      <h1 className="text-3xl font-bold mb-6">Meme Generator</h1>
      <p className="text-gray-600 mb-8 max-w-2xl text-center">
        Upload an image, add rectangles, and submit the annotated image to the server.
      </p>
      <ImageAnnotator />
    </main>
  )
}
