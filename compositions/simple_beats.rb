use_osc "decaura.local", 6005

live_loop :hard_beats do
  # sync :pont_aeri_section
  # sleep 4
  # Play hard drum beats
  with_fx :reverb, room: 0.6, mix: 0.5 do
    sample :bd_haus, rate: 1.5, amp: 1
    osc "/hello/world"    
    sleep 1
    sample :bd_zome, rate: 1, amp: 0.8, phase: 0.5
    sleep 1
  end
end
