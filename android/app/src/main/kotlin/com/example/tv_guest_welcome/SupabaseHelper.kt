package com.example.tv_guest_welcome

import okhttp3.*
import org.json.JSONArray
import java.io.IOException

class SupabaseHelper {
    private val client = OkHttpClient()
    private val url = "https://cewbmexcmhrogbvyfvrg.supabase.co/rest/v1/guests"
    private val apiKey = "sb_publishable_MCDhff2Dztq4pp3ASoWX3A_inNp10mx"

    fun fetchGuestName(roomNumber: String, callback: (String?) -> Unit) {
        val request = Request.Builder()
            .url("$url?room_number=eq.$roomNumber&select=full_name")
            .addHeader("apikey", apiKey)
            .addHeader("Authorization", "Bearer $apiKey")
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                callback(null)
            }

            override fun onResponse(call: Call, response: Response) {
                val body = response.body?.string()
                try {
                    val jsonArray = JSONArray(body)
                    if (jsonArray.length() > 0) {
                        val fullName = jsonArray.getJSONObject(0).getString("full_name")
                        callback(fullName)
                    } else {
                        callback("")
                    }
                } catch (e: Exception) {
                    callback(null)
                }
            }
        })
    }
}
