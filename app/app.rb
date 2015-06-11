require 'sinatra'

get '/' do
  "Hello #{ENV['SERVER_COLOR']}"
end

get '/auth' do
  'Success'
end
