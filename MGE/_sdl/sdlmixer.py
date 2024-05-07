from ctypes import Structure, CFUNCTYPE, c_int, c_char_p, c_void_p, c_double, POINTER as _P
from .dll import DLL, find_path
try:
    from .sdl2 import Uint8, Uint16, Uint32, Sint16, SDL_bool, SDL_RWops, SDL_RWFromFile, SDL_version
except:
    pass

MIXERFunc = DLL(find_path("SDL2_mixer.dll")).bind_function

Mix_Fading = c_int
MIX_NO_FADING = 0
MIX_FADING_OUT = 1
MIX_FADING_IN = 2

class Mix_Chunk(Structure):
    _fields_ = [("allocated", c_int), ("abuf", _P(Uint8)), ("alen", Uint32), ("volume", Uint8)]

class Mix_Music(c_void_p):
    pass

Mix_EffectFunc_t = CFUNCTYPE(None, c_int, c_void_p, c_int, c_void_p)
Mix_EffectDone_t = CFUNCTYPE(None, c_int, c_void_p)
soundfont_function = CFUNCTYPE(c_int, c_char_p, c_void_p)

def Mix_Linked_Version(): return MIXERFunc("Mix_Linked_Version", None, _P(SDL_version))().contents

def Mix_Init(flags=0): return MIXERFunc("Mix_Init", [c_int], c_int)(flags)

def Mix_Quit(): return MIXERFunc("Mix_Quit")()

def Mix_OpenAudio(frequency, format, channels, chunksize): return MIXERFunc("Mix_OpenAudio", [c_int, Uint16, c_int, c_int], c_int)(frequency, format, channels, chunksize)

def Mix_OpenAudioDevice(frequency, format, channels, chunksize, device, allowed_changes): return MIXERFunc("Mix_OpenAudioDevice", [c_int, Uint16, c_int, c_int, c_char_p, c_int], c_int)(frequency, format, channels, chunksize, device, allowed_changes)

def Mix_AllocateChannels(numchans): return MIXERFunc("Mix_AllocateChannels", [c_int], c_int)(numchans)

def Mix_QuerySpec(frequency, format, channels): return MIXERFunc("Mix_QuerySpec", [_P(c_int), _P(Uint16), _P(c_int)], c_int)(frequency, format, channels)

def Mix_LoadWAV_RW(src, freesrc): return MIXERFunc("Mix_LoadWAV_RW", [_P(SDL_RWops), c_int], _P(Mix_Chunk))(src, freesrc)

def Mix_LoadWAV(file): return Mix_LoadWAV_RW(SDL_RWFromFile(file, b"rb"), 1)

def Mix_LoadMUS(file): return MIXERFunc("Mix_LoadMUS", [c_char_p], _P(Mix_Music))(file)

def Mix_LoadMUS_RW(src, freesrc): return MIXERFunc("Mix_LoadMUS_RW", [_P(SDL_RWops)], _P(Mix_Music))(src, freesrc)

def Mix_QuickLoad_WAV(mem): return MIXERFunc("Mix_QuickLoad_WAV", [_P(Uint8)], _P(Mix_Chunk))(mem)

def Mix_QuickLoad_RAW(mem, len): return MIXERFunc("Mix_QuickLoad_RAW", [_P(Uint8), Uint32], _P(Mix_Chunk))(mem, len)

def Mix_FreeChunk(chunk): return MIXERFunc("Mix_FreeChunk", [_P(Mix_Chunk)])(chunk)
    
def Mix_FreeMusic(music): return MIXERFunc("Mix_FreeMusic", [_P(Mix_Music)])(music)

def Mix_GetNumChunkDecoders(): return MIXERFunc("Mix_GetNumChunkDecoders", None, c_int)()

def Mix_GetChunkDecoder(index): return MIXERFunc("Mix_GetChunkDecoder", [c_int], c_char_p)(index)

def Mix_HasChunkDecoder(name): return MIXERFunc("Mix_HasChunkDecoder", [c_char_p], SDL_bool)(name)

def Mix_GetNumMusicDecoders(): return MIXERFunc("Mix_GetNumMusicDecoders", None, c_int)()

def Mix_GetMusicDecoder(index): return MIXERFunc("Mix_GetMusicDecoder", [c_int], c_char_p)(index)

def Mix_HasMusicDecoder(name): return MIXERFunc("Mix_HasMusicDecoder", [c_char_p], SDL_bool)(name)

def Mix_GetMusicTitle(music): return MIXERFunc("Mix_GetMusicTitle", [_P(Mix_Music)], c_char_p)(music)

def Mix_GetMusicTitleTag(music): return MIXERFunc("Mix_GetMusicTitleTag", [_P(Mix_Music)], c_char_p)(music)

def Mix_GetMusicArtistTag(music): return MIXERFunc("Mix_GetMusicArtistTag", [_P(Mix_Music)], c_char_p)(music)

def Mix_GetMusicAlbumTag(music): return MIXERFunc("Mix_GetMusicAlbumTag", [_P(Mix_Music)], c_char_p)(music)

def Mix_GetMusicCopyrightTag(music): return MIXERFunc("Mix_GetMusicCopyrightTag", [_P(Mix_Music)], c_char_p)(music)

def Mix_SetPostMix(mix_func, arg): return MIXERFunc("Mix_SetPostMix", [mix_func, c_void_p])(mix_func, arg)

def Mix_HookMusic(mix_func, arg): return MIXERFunc("Mix_HookMusic", [mix_func, c_void_p])(mix_func, arg)

def Mix_HookMusicFinished(music_finished): return MIXERFunc("Mix_HookMusicFinished", [music_finished])(music_finished)

def Mix_GetMusicHookData(): return MIXERFunc("Mix_GetMusicHookData", None, c_void_p)()

def Mix_ChannelFinished(channel_finished): return MIXERFunc("Mix_ChannelFinished", [channel_finished])(channel_finished)

def Mix_RegisterEffect(chan, f, d, arg): return MIXERFunc("Mix_RegisterEffect", [c_int, Mix_EffectFunc_t, Mix_EffectDone_t, c_void_p], c_int)(chan, f, d, arg)

def Mix_UnregisterEffect(channel, f): return MIXERFunc("Mix_UnregisterEffect", [c_int, Mix_EffectFunc_t], c_int)(channel, f)

def Mix_UnregisterAllEffects(channel): return MIXERFunc("Mix_UnregisterAllEffects", [c_int])(channel)

def Mix_SetPanning(channel, left, right): return MIXERFunc("Mix_SetPanning", [c_int, Uint8, Uint8], c_int)(channel, left, right)

def Mix_SetPosition(channel, angle, distance): return MIXERFunc("Mix_SetPosition", [c_int, Sint16, Uint8], c_int)(channel, angle, distance)

def Mix_SetDistance(channel, distance): return MIXERFunc("Mix_SetDistance", [c_int, Uint8])(channel, distance)

def Mix_SetReverseStereo(channel, flip): return MIXERFunc("Mix_SetReverseStereo", [c_int, c_int], c_int)(channel, flip)

def Mix_ReserveChannels(num): return MIXERFunc("Mix_ReserveChannels", [c_int], c_int)(num)

def Mix_GroupChannel(which, tag): return MIXERFunc("Mix_GroupChannel", [c_int, c_int], c_int)(which, tag)

def Mix_GroupChannels(from_, to, tag): return MIXERFunc("Mix_GroupChannels", [c_int, c_int, c_int], c_int)(from_, to, tag)

def Mix_GroupAvailable(tag): return MIXERFunc("Mix_GroupAvailable", [c_int], c_int)(tag)

def Mix_GroupCount(tag): return MIXERFunc("Mix_GroupCount", [c_int], c_int)(tag)

def Mix_GroupOldest(tag): return MIXERFunc("Mix_GroupOldest", [c_int], c_int)(tag)

def Mix_GroupNewer(tag): return MIXERFunc("Mix_GroupNewer", [c_int], c_int)(tag)

def Mix_PlayChannelTimed(channel, chunk, loops, ticks): return MIXERFunc("Mix_PlayChannelTimed", [c_int, _P(Mix_Chunk), c_int, c_int], c_int)(channel, chunk, loops, ticks)

def Mix_PlayChannel(channel, chunk, loops): return MIXERFunc("Mix_PlayChannel", [c_int, _P(Mix_Chunk), c_int], c_int)(channel, chunk, loops)

def Mix_PlayMusic(music, loops): return MIXERFunc("Mix_PlayMusic", [_P(Mix_Music), c_int], c_int)(music, loops)

def Mix_FadeInMusic(music, loops, ms): return MIXERFunc("Mix_FadeInMusic", [_P(Mix_Music), c_int, c_int], c_int)(music, loops, ms)

def Mix_FadeInMusicPos(music, loops, ms, position): return MIXERFunc("Mix_FadeInMusicPos", [_P(Mix_Music), c_int, c_int, c_double], c_int)(music, loops, ms, position)

def Mix_FadeInChannelTimed(channel, chunk, loops, ms, ticks): return MIXERFunc("Mix_FadeInChannelTimed", [c_int, _P(Mix_Chunk), c_int, c_int, c_int], c_int)(channel, chunk, loops, ms, ticks)

def Mix_FadeInChannel(channel, chunk, loops, ms): return MIXERFunc("Mix_FadeInChannel", [c_int, _P(Mix_Chunk), c_int, c_int], c_int)(channel, chunk, loops, ms)

def Mix_Volume(channel, volume): return MIXERFunc("Mix_Volume", [c_int, c_int], c_int)(channel, volume)

def Mix_VolumeChunk(chunk, volume): return MIXERFunc("Mix_VolumeChunk", [_P(Mix_Chunk), c_int], c_int)(chunk, volume)

def Mix_VolumeMusic(volume): return MIXERFunc("Mix_VolumeMusic", [c_int], c_int)(volume)

def Mix_GetMusicVolume(music): return MIXERFunc("Mix_GetMusicVolume", [_P(Mix_Music)], c_int)(music)

def Mix_MasterVolume(volume): return MIXERFunc("Mix_MasterVolume", [c_int], c_int)(volume)

def Mix_HaltChannel(channel): return MIXERFunc("Mix_HaltChannel", [c_int], c_int)(channel)

def Mix_HaltGroup(tag): return MIXERFunc("Mix_HaltGroup", [c_int], c_int)(tag)

def Mix_HaltMusic(): return MIXERFunc("Mix_HaltMusic", None, c_int)()

def Mix_ExpireChannel(channel, ticks): return MIXERFunc("Mix_ExpireChannel", [c_int, c_int], c_int)(channel, ticks)

def Mix_FadeOutChannel(which, ms): return MIXERFunc("Mix_FadeOutChannel", [c_int, c_int], c_int)(which, ms)

def Mix_FadeOutGroup(tag, ms): return MIXERFunc("Mix_FadeOutGroup", [c_int, c_int], c_int)(tag, ms)

def Mix_FadeOutMusic(ms): return MIXERFunc("Mix_FadeOutMusic", [c_int], c_int)(ms)

def Mix_FadingMusic(): return MIXERFunc("Mix_FadingMusic", None, Mix_Fading)()

def Mix_FadingChannel(which): return MIXERFunc("Mix_FadingChannel", [c_int], Mix_Fading)(which)

def Mix_Pause(channel): return MIXERFunc("Mix_Pause", [c_int])(channel)

def Mix_Resume(channel): return MIXERFunc("Mix_Resume", [c_int])(channel)

def Mix_Paused(channel): return MIXERFunc("Mix_Paused", [c_int], c_int)(channel)

def Mix_PauseMusic(): return MIXERFunc("Mix_PauseMusic")()

def Mix_ResumeMusic(): return MIXERFunc("Mix_ResumeMusic")()

def Mix_RewindMusic(): return MIXERFunc("Mix_RewindMusic")()

def Mix_PausedMusic(): return MIXERFunc("Mix_PausedMusic", None, c_int)()

def Mix_ModMusicJumpToOrder(order): return MIXERFunc("Mix_ModMusicJumpToOrder", [c_int], c_int)(order)

def Mix_SetMusicPosition(position): return MIXERFunc("Mix_SetMusicPosition", [c_double], c_int)(position)

def Mix_GetMusicPosition(music): return MIXERFunc("Mix_GetMusicPosition", [_P(Mix_Music)], c_double)(music)

def Mix_MusicDuration(music): return MIXERFunc("Mix_MusicDuration", [_P(Mix_Music)], c_double)(music)

def Mix_GetMusicLoopStartTime(music): return MIXERFunc("Mix_GetMusicLoopStartTime", [_P(Mix_Music)], c_double)(music)

def Mix_GetMusicLoopEndTime(music): return MIXERFunc("Mix_GetMusicLoopEndTime", [_P(Mix_Music)], c_double)(music)

def Mix_GetMusicLoopLengthTime(music): return MIXERFunc("Mix_GetMusicLoopLengthTime", [_P(Mix_Music)], c_double)(music)

def Mix_Playing(channel): return MIXERFunc("Mix_Playing", [c_int], c_int)(channel)

def Mix_PlayingMusic(): return MIXERFunc("Mix_PlayingMusic", None, c_int)()

def Mix_SetMusicCMD(command): return MIXERFunc("Mix_SetMusicCMD", [c_char_p], c_int)(command)

def Mix_SetSynchroValue(value): return MIXERFunc("Mix_SetSynchroValue", [c_int], c_int)(value)

def Mix_GetSynchroValue(): return MIXERFunc("Mix_GetSynchroValue", None, c_int)()

def Mix_SetSoundFonts(paths): return MIXERFunc("Mix_SetSoundFonts", [c_char_p], c_int)(paths)

def Mix_GetSoundFonts(): return MIXERFunc("Mix_GetSoundFonts", None, c_char_p)()

def Mix_EachSoundFont(function, data): return MIXERFunc("Mix_EachSoundFont", [soundfont_function, c_void_p], c_int)(function, data)

def Mix_SetTimidityCfg(path): return MIXERFunc("Mix_SetTimidityCfg", [c_char_p], c_int)(path)

def Mix_GetTimidityCfg(): return MIXERFunc("Mix_GetTimidityCfg", None, c_char_p)()

def Mix_GetChunk(channel): return MIXERFunc("Mix_GetChunk", [c_int], _P(Mix_Chunk))(channel)

def Mix_CloseAudio(): return MIXERFunc("Mix_CloseAudio")()
