FROM ruby

RUN gem install bundler && \
    mkdir -p /src

ADD app/Gemfile /src/Gemfile
RUN cd /src && bundle install --path vendor/bundle

ADD app /src

EXPOSE 4567

WORKDIR /src

CMD ["bundle", "exec", "ruby", "app.rb", "-e", "production"]
