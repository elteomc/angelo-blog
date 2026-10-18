function Para(el)
  local text = pandoc.utils.stringify(el)
  if text:match("^The complete series") or text:match("^Previous:") or text:match("^Next:") then
    return {}
  end
end
