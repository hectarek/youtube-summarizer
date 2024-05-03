"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { SummaryFormProps } from "@/types"


const youtubeUrlRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]+(&[\w-]+)*$/;

const FormSchema = z.object({
  url: z.string().regex(youtubeUrlRegex, { message: "Invalid YouTube URL" })
})

export function SummaryForm({ setSummaryData }: SummaryFormProps) {

  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      url: "",
    },
  })

  const onSubmit = (values: z.infer<typeof FormSchema>) => {
    setSummaryData({ values })
  };

  return (
    <Form {...form}>
      <h1 className="text-3xl font-bold pb-8">YouTube Video Summarizer</h1>
      <form onSubmit={form.handleSubmit(onSubmit)} className="w-full space-y-6 md:w-2/3">
        <FormField
          control={form.control}
          name="url"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Enter Video URL to Summarize</FormLabel>
              <FormControl>
                <Input placeholder="YouTube URL" {...field} />
              </FormControl>
              <FormDescription>
                It will take the video url and create a summary of the video based on its transcript.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Generate Transcript</Button>
      </form>
    </Form>
  )
}
