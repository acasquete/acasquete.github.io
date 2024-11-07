require 'date'

module Jekyll
  module SpanishDateFilter
    MONTHS = %w[enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre]

    def date_in_spanish(date)
      parsed_date = Date.parse(date.to_s)
      "#{parsed_date.day} de #{MONTHS[parsed_date.month - 1]} de #{parsed_date.year}"
    end
  end
end

Liquid::Template.register_filter(Jekyll::SpanishDateFilter)